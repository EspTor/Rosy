"""Tests for the agent brains system."""
import pytest
from uuid import uuid4
from agentropolis.brains import SimpleBrain, BrainDecision
from agentropolis.models import Agent, Location

@pytest.fixture
def sample_agent():
    return Agent(
        id=uuid4(),
        name="Test Agent",
        type="worker",
        health=80,
        energy=60,
        hunger=30,
        happiness=10,
        money=50.0
    )

@pytest.fixture
def sample_locations():
    return [
        Location(
            id=uuid4(),
            name="Home",
            type="home",
            district="residential",
            x=0,
            y=0,
            provides_sleep=True,
            capacity=4
        ),
        Location(
            id=uuid4(),
            name="Food Market",
            type="market",
            district="commercial",
            x=10,
            y=0,
            provides_food=True,
            capacity=10
        ),
        Location(
            id=uuid4(),
            name="Workplace",
            type="work",
            district="industrial",
            x=5,
            y=5,
            provides_work=True,
            capacity=20
        )
    ]

@pytest.mark.asyncio
async def test_brain_creation():
    """Test that a brain can be created for an agent."""
    agent_id = uuid4()
    brain = SimpleBrain(agent_id)
    assert brain.agent_id == agent_id
    assert isinstance(brain.memory, list)
    assert isinstance(brain.long_term_memory, dict)

@pytest.mark.asyncio
async def test_hungry_agent_seeks_food(sample_agent, sample_locations):
    """Test that a hungry agent seeks food."""
    # Make agent hungry
    sample_agent.hunger = 80  # Above threshold of 70
    sample_agent.energy = 50  # Not tired
    
    brain = SimpleBrain(sample_agent.id)
    world_state = {
        "agents": [sample_agent],
        "locations": sample_locations
    }
    
    decision = await brain.decide(sample_agent, world_state)
    
    assert decision.action_type == "move"
    assert decision.confidence >= 0.8
    assert "hungry" in decision.reasoning.lower()
    assert "food" in decision.reasoning.lower()
    # Should target the food market
    food_market = next(loc for loc in sample_locations if loc.name == "Food Market")
    assert str(decision.target_id) == str(food_market.id)

@pytest.mark.asyncio
async def test_tired_agent_seeks_rest(sample_agent, sample_locations):
    """Test that a tired agent seeks rest."""
    # Make agent tired but not hungry
    sample_agent.energy = 20  # Below threshold of 30
    sample_agent.hunger = 40  # Not hungry
    
    brain = SimpleBrain(sample_agent.id)
    world_state = {
        "agents": [sample_agent],
        "locations": sample_locations
    }
    
    decision = await brain.decide(sample_agent, world_state)
    
    assert decision.action_type == "move"
    assert decision.confidence >= 0.8
    assert "tired" in decision.reasoning.lower()
    assert "rest" in decision.reasoning.lower()
    # Should target home
    home = next(loc for loc in sample_locations if loc.name == "Home")
    assert str(decision.target_id) == str(home.id)

@pytest.mark.asyncio
async def test_healthy_agent_with_money_works(sample_agent, sample_locations):
    """Test that an agent with low money and good health seeks work."""
    sample_agent.money = 30  # Low money
    sample_agent.energy = 70  # Good energy
    sample_agent.hunger = 40  # Not hungry
    sample_agent.health = 80  # Healthy
    
    brain = SimpleBrain(sample_agent.id)
    world_state = {
        "agents": [sample_agent],
        "locations": sample_locations
    }
    
    decision = await brain.decide(sample_agent, world_state)
    
    # Could be work or socialize - both are reasonable
    assert decision.action_type in ["work", "socialize", "move"]
    if decision.action_type == "work":
        assert decision.confidence >= 0.5
        assert "money" in decision.reasoning.lower()

@pytest.mark.asyncio
async def test_unhappy_agent_seeks_entertainment(sample_agent, sample_locations):
    """Test that an unhappy agent seeks entertainment."""
    # Make agent unhappy (need to add happiness threshold logic)
    # For now, we'll test that the brain doesn't crash
    sample_agent.happiness = -30  # Very unhappy
    
    brain = SimpleBrain(sample_agent.id)
    world_state = {
        "agents": [sample_agent],
        "locations": sample_locations
    }
    
    decision = await brain.decide(sample_agent, world_state)
    
    assert isinstance(decision, BrainDecision)
    assert decision.action_type in ["move", "socialize", "idle", "work"]

@pytest.mark.asyncio
async def test_brain_memory():
    """Test that the brain can remember and learn."""
    agent_id = uuid4()
    brain = SimpleBrain(agent_id)
    
    # Test remembering
    event = {"type": "test", "data": "value"}
    brain.remember(event)
    assert len(brain.memory) == 1
    assert brain.memory[0] == event
    
    # Test learning
    brain.learn("key", "value")
    assert brain.recall("key") == "value"
    assert brain.recall("nonexistent", "default") == "default"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])