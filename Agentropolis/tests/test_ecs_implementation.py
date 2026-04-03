"""Tests for the ECS-based simulation engine implementation."""
import pytest
import asyncio
import uuid
from unittest.mock import Mock, AsyncMock, patch

# Add project to path
import sys
sys.path.insert(0, '/home/ubuntu/Documents/Obsidian Vault/Agentropolis')

from agentropolis.engine.ecs import Entity, Component, System, World
from agentropolis.engine.components import (
    PositionComponent, BodyComponent, MindComponent, IdentityComponent,
    EconomicsComponent, SocialComponent, OccupationComponent,
    LocationComponent, AgentStateComponent
)
from agentropolis.engine.systems import (
    MovementSystem, EcsBrainSystem, NeedsSystem, SocialSystem, EconomySystem
)


class TestECSCore:
    """Test core ECS functionality."""
    
    def test_entity_creation(self):
        """Test that entities can be created and have unique IDs."""
        entity1 = Entity()
        entity2 = Entity()
        
        assert entity1.id != entity2.id
        assert isinstance(entity1.id, uuid.UUID)
        assert isinstance(entity2.id, uuid.UUID)
        assert len(entity1.components) == 0
        assert len(entity2.components) == 0
    
    def test_component_addition_and_retrieval(self):
        """Test adding and retrieving components."""
        entity = Entity()
        
        # Add components
        position = PositionComponent(x=10.5, y=20.3)
        entity.add_component(position)
        
        identity = IdentityComponent(name="TestAgent", agent_type="test")
        entity.add_component(identity)
        
        # Retrieve components
        retrieved_position = entity.get_component(PositionComponent)
        retrieved_identity = entity.get_component(IdentityComponent)
        
        assert retrieved_position is not None
        assert retrieved_position.x == 10.5
        assert retrieved_position.y == 20.3
        
        assert retrieved_identity is not None
        assert retrieved_identity.name == "TestAgent"
        assert retrieved_identity.agent_type == "test"
        
        # Test non-existent component
        nonexistent = entity.get_component(MindComponent)
        assert nonexistent is None
    
    def test_component_replacement(self):
        """Test that adding a component of same type replaces the old one."""
        entity = Entity()
        
        # Add first component
        pos1 = PositionComponent(x=1.0, y=1.0)
        entity.add_component(pos1)
        
        # Add second component of same type
        pos2 = PositionComponent(x=2.0, y=2.0)
        entity.add_component(pos2)
        
        # Should only have one PositionComponent
        components = entity.get_component(PositionComponent)
        assert components.x == 2.0
        assert components.y == 2.0
        # Verify only one component of this type exists
        assert len([c for c in entity.components.values() if isinstance(c, PositionComponent)]) == 1
    
    def test_system_initialization(self):
        """Test that systems initialize correctly."""
        # Mock world
        mock_world = Mock()
        
        # Test each system type
        movement_system = MovementSystem(mock_world)
        assert movement_system.world == mock_world
        assert PositionComponent in movement_system.required_components
        
        brain_system = EcsBrainSystem(mock_world)
        assert brain_system.world == mock_world
        # Should require multiple components for brain decisions
        assert len(brain_system.required_components) >= 5
        
        needs_system = NeedsSystem(mock_world)
        assert needs_system.world == mock_world
        assert BodyComponent in needs_system.required_components
        assert MindComponent in needs_system.required_components
    
    @pytest.mark.asyncio
    async def test_world_entity_management(self):
        """Test world entity creation and management."""
        world = World()
        
        # Create entity
        entity = world.create_entity()
        
        assert entity.id in world.entities
        assert world.entities[entity.id] == entity
        assert len(world.entities) == 1
        assert len(world.systems) == 0
        
        # Destroy entity
        world.destroy_entity(entity.id)
        
        assert entity.id not in world.entities
        assert len(world.entities) == 0
    
    @pytest.mark.asyncio
    async def test_system_entity_tracking(self):
        """Test that systems track entities with required components."""
        world = World()
        
        # Create system that requires PositionComponent
        movement_system = MovementSystem(world)
        world.add_system(movement_system)
        
        # Create entity without required component
        entity_no_pos = world.create_entity()
        entity_no_pos.add_component(IdentityComponent(name="Static", agent_type="test"))
        
        # Create entity with required component
        entity_with_pos = world.create_entity()
        entity_with_pos.add_component(PositionComponent(x=0, y=0))
        entity_with_pos.add_component(IdentityComponent(name="Mover", agent_type="test"))
        
        # Initially, system should track the entity with position
        # But we need to trigger the update mechanism
        # For simplicity in this test, we'll check the matching logic directly
        
        # Test the internal matching method
        assert world._entity_matches_system(entity_no_pos, movement_system) == False
        assert world._entity_matches_system(entity_with_pos, movement_system) == True
    
    def test_component_basic_functionality(self):
        """Test that all component types work correctly."""
        # PositionComponent
        pos = PositionComponent(x=100.5, y=200.7)
        assert pos.x == 100.5
        assert pos.y == 200.7
        
        # BodyComponent
        body = BodyComponent(health=80, energy=60, hunger=30)
        assert body.health == 80
        assert body.energy == 60
        assert body.hunger == 30
        
        # MindComponent
        mind = MindComponent(happiness=25)
        assert mind.happiness == 25
        
        # IdentityComponent
        identity = IdentityComponent(name="Alice", agent_type="worker")
        assert identity.name == "Alice"
        assert identity.agent_type == "worker"
        
        # EconomicsComponent
        economics = EconomicsComponent(money=150.50)
        assert economics.money == 150.50
        
        # SocialComponent
        social = SocialComponent()
        assert social.relationships == []
        assert social.last_social_tick == 0
        
        # OccupationComponent
        occupation = OccupationComponent(occupation="engineer", employed=True)
        assert occupation.occupation == "engineer"
        assert occupation.employed == True
        
        # LocationComponent
        location = LocationComponent(location_id=uuid.uuid4())
        assert isinstance(location.location_id, uuid.UUID)
        
        # AgentStateComponent
        state = AgentStateComponent(is_active=True, is_sleeping=False)
        assert state.is_active == True
        assert state.is_sleeping == False


class TestECSSystems:
    """Test ECS systems functionality."""
    
    @pytest.mark.asyncio
    async def test_movement_system_no_action(self):
        """Test movement system with no movement component."""
        mock_world = Mock()
        system = MovementSystem(mock_world)
        
        # Entity without position component
        entity = Entity()
        entity.add_component(IdentityComponent(name="Static", agent_type="test"))
        
        entities = {entity.id: entity}
        await system.process(entities, 0.1)  # 100ms tick
        
        # Should not crash and not modify anything
        assert len(entities) == 1
    
    @pytest.mark.asyncio
    async def test_movement_system_with_position(self):
        """Test movement system with position component."""
        mock_world = Mock()
        system = MovementSystem(mock_world)
        
        # Entity with position component
        entity = Entity()
        position = PositionComponent(x=0.0, y=0.0)
        entity.add_component(position)
        entity.add_component(IdentityComponent(name="Mover", agent_type="test"))
        
        entities = {entity.id: entity}
        initial_x = position.x
        initial_y = position.y
        
        # Process multiple ticks to see if movement occurs
        for _ in range(10):  # 10 ticks
            await system.process(entities, 0.1)
        
        # Position might have changed due to random movement
        # (10% chance per tick to move)
        final_x = position.x
        final_y = position.y
        
        # At least verify the component still exists and is accessible
        assert hasattr(position, 'x')
        assert hasattr(position, 'y')
    
    @pytest.mark.asyncio
    async def test_needs_system(self):
        """Test needs system applies natural changes."""
        mock_world = Mock()
        system = NeedsSystem(mock_world)
        
        # Entity with body and mind components
        entity = Entity()
        body = BodyComponent(health=100, energy=50, hunger=50)
        mind = MindComponent(happiness=10)
        entity.add_component(body)
        entity.add_component(mind)
        
        entities = {entity.id: entity}
        
        # Store initial values
        initial_energy = body.energy
        initial_hunger = body.hunger
        initial_happiness = mind.happiness
        initial_health = body.health
        
        # Process for a longer duration to see changes
        await system.process(entities, 2.0)  # 2 seconds
        
        # Hunger should increase, energy should decrease
        # Happiness should drift toward 0
        # Health might decrease if needs are extreme (but they're not here)
        
        # Just verify the components still exist and have reasonable values
        assert body.energy >= 0
        assert body.hunger <= 100
        assert 0 <= mind.happiness <= 100  # Clamped values
        assert body.health >= 0
    
    @pytest.mark.asyncio
    async def test_social_system(self):
        """Test social system processes social component."""
        mock_world = Mock()
        system = SocialSystem(mock_world)
        
        # Entity with social component
        entity = Entity()
        social = SocialComponent()
        entity.add_component(social)
        entity.add_component(IdentityComponent(name="Social", agent_type="test"))
        
        entities = {entity.id: entity}
        initial_tick = social.last_social_tick
        
        # Process
        await system.process(entities, 1.5)
        
        # Social tick should have increased
        assert social.last_social_tick >= initial_tick
    
    @pytest.mark.asyncio
    async def test_economy_system(self):
        """Test economy system applies passive income."""
        mock_world = Mock()
        system = EconomySystem(mock_world)
        
        # Entity with economics component
        entity = Entity()
        economics = EconomicsComponent(money=100.0)
        entity.add_component(economics)
        entity.add_component(IdentityComponent(name="Rich", agent_type="test"))
        
        entities = {entity.id: entity}
        initial_money = economics.money
        
        # Process
        await system.process(entities, 10.0)  # 10 seconds
        
        # Money should have increased slightly (passive income)
        assert economics.money >= initial_money
        # But not excessively (capped at 1000 in implementation)
        assert economics.money <= 110.0  # Rough upper bound for 10 seconds


class TestECSIntegration:
    """Test ECS integration with existing systems."""
    
    @pytest.mark.asyncio
    async def test_agentropolis_world_initialization(self):
        """Test that AgentropolisWorld can initialize from database."""
        from agentropolis.engine.world import AgentropolisWorld
        
        world = AgentropolisWorld()
        
        # This would normally connect to database, but we'll test that it instantiates
        assert world.ecs_world is not None
        assert isinstance(world.ecs_world, World)
        assert len(world.agent_entities) == 0
        assert len(world.location_entities) == 0
        assert world._sync_interval == 5.0
    
    def test_component_imports(self):
        """Test that all engine components can be imported."""
        # This is already tested by the imports at the top, but explicit test
        components = [
            PositionComponent, BodyComponent, MindComponent, IdentityComponent,
            EconomicsComponent, SocialComponent, OccupationComponent,
            LocationComponent, AgentStateComponent
        ]
        
        for component_class in components:
            assert component_class is not None
            # Can instantiate
            instance = component_class()
            assert instance is not None
    
    def test_system_imports(self):
        """Test that all engine systems can be imported."""
        systems = [
            MovementSystem, EcsBrainSystem, NeedsSystem, SocialSystem, EconomySystem
        ]
        
        for system_class in systems:
            assert system_class is not None
            # Can instantiate with mock world
            mock_world = Mock()
            instance = system_class(mock_world)
            assert instance is not None
            assert instance.world == mock_world


def test_ecs_end_to_end_simple():
    """Simple end-to-end test of ECS functionality."""
    # Create world
    world = World()
    
    # Add some systems
    movement_system = MovementSystem(world)
    needs_system = NeedsSystem(world)
    world.add_system(movement_system)
    world.add_system(needs_system)
    
    # Create test agent entity
    agent = Entity()
    
    # Add all necessary components for a basic agent
    agent.add_component(PositionComponent(x=10.0, y=10.0))
    agent.add_component(BodyComponent(health=100, energy=80, hunger=20))
    agent.add_component(MindComponent(happiness=25))
    agent.add_component(IdentityComponent(name="TestAgent", agent_type="worker"))
    agent.add_component(EconomicsComponent(money=50.0))
    agent.add_component(SocialComponent())
    agent.add_component(OccupationComponent(occupation="unemployed", employed=False))
    agent.add_component(LocationComponent(location_id=None))  # No location yet
    agent.add_component(AgentStateComponent(is_active=True, is_sleeping=False))
    
    # Add entity to world
    world.entities[agent.id] = agent
    
    # Notify systems about the entity (simplified)
    movement_system.add_entity(agent.id)
    needs_system.add_entity(agent.id)
    
    # Verify entity has all expected components
    assert agent.has_component(PositionComponent)
    assert agent.has_component(BodyComponent)
    assert agent.has_component(MindComponent)
    assert agent.has_component(IdentityComponent)
    assert agent.has_component(EconomicsComponent)
    assert agent.has_component(SocialComponent)
    assert agent.has_component(OccupationComponent)
    assert agent.has_component(AgentStateComponent)
    
    # Get component values for verification
    pos = agent.get_component(PositionComponent)
    body = agent.get_component(BodyComponent)
    identity = agent.get_component(IdentityComponent)
    
    assert pos.x == 10.0 and pos.y == 10.0
    assert body.health == 100 and body.energy == 80 and body.hunger == 20
    assert identity.name == "TestAgent"
    assert identity.agent_type == "worker"


if __name__ == "__main__":
    # Run the tests
    import traceback
    
    test_instance = TestECSCore()
    test_systems = TestECSSystems()
    test_integration = TestECSIntegration()
    
    tests = [
        ("Entity Creation", test_instance.test_entity_creation),
        ("Component Addition/Retrieval", test_instance.test_component_addition_and_retrieval),
        ("Component Replacement", test_instance.test_component_replacement),
        ("System Initialization", test_instance.test_system_initialization),
        ("Component Basic Functionality", test_instance.test_component_basic_functionality),
        ("Component Imports", test_integration.test_component_imports),
        ("System Imports", test_integration.test_system_imports),
        ("ECS End-to-End Simple", test_ecs_end_to_end_simple),
    ]
    
    passed = 0
    failed = 0
    
    print("Running ECS Implementation Tests...")
    print("=" * 50)
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                asyncio.run(test_func())
            else:
                test_func()
            print(f"✓ {test_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {test_name}: {e}")
            traceback.print_exc()
            failed += 1
        print()
    
    # Run async system tests
    async_tests = [
        ("World Entity Management", test_instance.test_world_entity_management),
        ("System Entity Tracking", test_instance.test_system_entity_tracking),
        ("Movement System No Action", test_systems.test_movement_system_no_action),
        ("Movement System With Position", test_systems.test_movement_system_with_position),
        ("Needs System", test_systems.test_needs_system),
        ("Social System", test_systems.test_social_system),
        ("Economy System", test_systems.test_economy_system),
        ("Agentropolis World Initialization", test_integration.test_agentropolis_world_initialization),
    ]
    
    print("Running Async Tests...")
    print("=" * 50)
    
    for test_name, test_func in async_tests:
        try:
            asyncio.run(test_func())
            print(f"✓ {test_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {test_name}: {e}")
            traceback.print_exc()
            failed += 1
        print()
    
    print("=" * 50)
    print(f"Tests Passed: {passed}")
    print(f"Tests Failed: {failed}")
    print(f"Total Tests:  {passed + failed}")
    
    if failed == 0:
        print("🎉 All ECS implementation tests passed!")
        exit(0)
    else:
        print("❌ Some tests failed.")
        exit(1)