"""Model tests.""""""
import pytest
from agentropolis.models import Agent

@pytest.mark.asyncio
async def test_agent_creation(db_session, sample_agent_data):
    agent = Agent(**sample_agent_data)
    db_session.add(agent)
    await db_session.commit()
    result = await db_session.get(Agent, agent.id)
    assert result.name == "Test"

if __name__ == "__main__":
    import pytest as pt; pt.main([__file__, "-v"])
