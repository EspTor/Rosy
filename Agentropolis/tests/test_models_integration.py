"""Integration tests for models and relationships."""
import pytest
from sqlalchemy.orm import selectinload
from agentropolis.models import Agent, Location, Relationship

@pytest.mark.asyncio
async def test_agent_location_relationship(db_session):
    """Test agent-location foreign key relationship."""
    # Create location
    location = Location(
        name="Test Location",
        type="test",
        district="test",
        x=10.0,
        y=20.0
    )
    db_session.add(location)
    await db_session.commit()

    # Create agent with location
    agent = Agent(
        name="Test Agent",
        type="test",
        location_id=location.id
    )
    db_session.add(agent)
    await db_session.commit()

    # Verify relationship
    result = await db_session.get(Agent, agent.id)
    assert result.location is not None
    assert result.location.id == location.id
    assert result.location.name == "Test Location"

@pytest.mark.asyncio
async def test_agent_relationship_self_referential(db_session):
    """Test agent-to-agent relationships."""
    # Create two agents
    agent_a = Agent(name="Alice", type="test")
    agent_b = Agent(name="Bob", type="test")
    db_session.add_all([agent_a, agent_b])
    await db_session.commit()

    # Create relationship
    rel = Relationship(
        agent_a_id=agent_a.id,
        agent_b_id=agent_b.id,
        type="friend",
        trust=0.8,
        affection=0.5
    )
    db_session.add(rel)
    await db_session.commit()

    # Verify
    result = await db_session.get(Relationship, (agent_a.id, agent_b.id))
    assert result.type == "friend"
    assert result.agent_a.name == "Alice"
    assert result.agent_b.name == "Bob"

    # Check back-populates: load relationships within the same session using eager loading
    from sqlalchemy import select
    stmt = select(Agent).where(Agent.id == agent_a.id).options(selectinload(Agent.relationships_as_a))
    alice = await db_session.execute(stmt)
    alice_obj = alice.scalar_one()
    assert len(alice_obj.relationships_as_a) == 1
    assert alice_obj.relationships_as_a[0].agent_b_id == agent_b.id

if __name__ == "__main__":
    import pytest as pt
    pt.main([__file__, "-v"])
