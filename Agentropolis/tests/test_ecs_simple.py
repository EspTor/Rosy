"""Simple tests for ECS implementation that work without complex mocking."""
import sys
import asyncio
import uuid

# Add project to path
sys.path.insert(0, '/home/ubuntu/Documents/Obsidian Vault/Agentropolis')

def test_basic_imports():
    """Test that we can import the core ECS components."""
    print("Testing basic imports...")
    
    try:
        from agentropolis.engine.ecs import Entity, Component, System, World
        print("✓ ECS core imports successful")
    except Exception as e:
        print(f"✗ ECS core import failed: {e}")
        return False
    
    try:
        from agentropolis.engine.components import (
            PositionComponent, BodyComponent, MindComponent, IdentityComponent,
            EconomicsComponent, SocialComponent, OccupationComponent,
            LocationComponent, AgentStateComponent
        )
        print("✓ ECS components imports successful")
    except Exception as e:
        print(f"✗ ECS components import failed: {e}")
        return False
        
    try:
        from agentropolis.engine.systems import (
            MovementSystem, EcsBrainSystem, NeedsSystem, SocialSystem, EconomySystem
        )
        print("✓ ECS systems imports successful")
    except Exception as e:
        print(f"✗ ECS systems import failed: {e}")
        return False
    
    try:
        from agentropolis.engine.world import AgentropolisWorld
        print("✓ ECS world imports successful")
    except Exception as e:
        print(f"✗ ECS world import failed: {e}")
        return False
        
    try:
        from agentropolis.engine import World as EngineWorld, Entity as EngineEntity
        print("✓ Engine package imports successful")
    except Exception as e:
        print(f"✗ Engine package import failed: {e}")
        return False
    
    return True

def test_ecs_core_functionality():
    """Test basic ECS functionality without external dependencies."""
    print("\nTesting ECS core functionality...")
    
    from agentropolis.engine.ecs import Entity, Component
    from agentropolis.engine.components import PositionComponent, IdentityComponent
    
    # Test entity creation
    entity = Entity()
    assert entity.id is not None
    print(f"✓ Entity created: {entity.id}")
    
    # Test component addition
    position = PositionComponent(x=10.0, y=20.0)
    entity.add_component(position)
    assert entity.has_component(PositionComponent)
    print("✓ PositionComponent added")
    
    identity = IdentityComponent(name="TestAgent", agent_type="test")
    entity.add_component(identity)
    assert entity.has_component(IdentityComponent)
    print("✓ IdentityComponent added")
    
    # Test component retrieval
    retrieved_pos = entity.get_component(PositionComponent)
    retrieved_identity = entity.get_component(IdentityComponent)
    
    assert retrieved_pos is not None
    assert retrieved_pos.x == 10.0
    assert retrieved_pos.y == 20.0
    print("✓ PositionComponent retrieved correctly")
    
    assert retrieved_identity is not None
    assert retrieved_identity.name == "TestAgent"
    assert retrieved_identity.agent_type == "test"
    print("✓ IdentityComponent retrieved correctly")
    
    # Test component replacement
    position2 = PositionComponent(x=30.0, y=40.0)
    entity.add_component(position2)
    # Should still only have one PositionComponent
    pos_count = sum(1 for c in entity.components.values() 
                   if isinstance(c, PositionComponent))
    assert pos_count == 1
    final_pos = entity.get_component(PositionComponent)
    assert final_pos.x == 30.0
    assert final_pos.y == 40.0
    print("✓ Component replacement works")
    
    print("✓ All ECS core functionality tests passed")
    return True

def test_all_component_types():
    """Test that all component types can be instantiated and have expected attributes."""
    print("\nTesting all component types...")
    
    from agentropolis.engine.components import (
        PositionComponent, BodyComponent, MindComponent, IdentityComponent,
        EconomicsComponent, SocialComponent, OccupationComponent,
        LocationComponent, AgentStateComponent
    )
    
    # PositionComponent
    pos = PositionComponent(x=1.5, y=2.5)
    assert pos.x == 1.5
    assert pos.y == 2.5
    print("✓ PositionComponent")
    
    # BodyComponent
    body = BodyComponent(health=100, energy=50, hunger=30)
    assert body.health == 100
    assert body.energy == 50
    assert body.hunger == 30
    print("✓ BodyComponent")
    
    # MindComponent
    mind = MindComponent(happiness=25)
    assert mind.happiness == 25
    print("✓ MindComponent")
    
    # IdentityComponent
    identity = IdentityComponent(name="TestBot", agent_type="robot")
    assert identity.name == "TestBot"
    assert identity.agent_type == "robot"
    print("✓ IdentityComponent")
    
    # EconomicsComponent
    economics = EconomicsComponent(money=100.50)
    assert economics.money == 100.50
    print("✓ EconomicsComponent")
    
    # SocialComponent
    social = SocialComponent()
    assert isinstance(social.relationships, list)
    assert social.last_social_tick == 0
    print("✓ SocialComponent")
    
    # OccupationComponent
    occupation = OccupationComponent(occupation="programmer", employed=True)
    assert occupation.occupation == "programmer"
    assert occupation.employed == True
    print("✓ OccupationComponent")
    
    # LocationComponent
    test_uuid = uuid.uuid4()
    location = LocationComponent(location_id=test_uuid)
    assert location.location_id == test_uuid
    print("✓ LocationComponent")
    
    # AgentStateComponent
    state = AgentStateComponent(is_active=True, is_sleeping=False)
    assert state.is_active == True
    assert state.is_sleeping == False
    print("✓ AgentStateComponent")
    
    print("✓ All component types work correctly")
    return True

def test_systems_can_be_instantiated():
    """Test that ECS systems can be instantiated with a mock world."""
    print("\nTesting ECS system instantiation...")
    
    from agentropolis.engine.systems import (
        MovementSystem, EcsBrainSystem, NeedsSystem, SocialSystem, EconomySystem
    )
    
    # Simple mock world
    class MockWorld:
        def __init__(self):
            self.entities = {}
    
    mock_world = MockWorld()
    
    # Test each system
    try:
        movement = MovementSystem(mock_world)
        assert movement.world == mock_world
        print("✓ MovementSystem instantiated")
    except Exception as e:
        print(f"✗ MovementSystem failed: {e}")
        return False
        
    try:
        brain = EcsBrainSystem(mock_world)
        assert brain.world == mock_world
        print("✓ EcsBrainSystem instantiated")
    except Exception as e:
        print(f"✗ EcsBrainSystem failed: {e}")
        return False
        
    try:
        needs = NeedsSystem(mock_world)
        assert needs.world == mock_world
        print("✓ NeedsSystem instantiated")
    except Exception as e:
        print(f"✗ NeedsSystem failed: {e}")
        return False
        
    try:
        social = SocialSystem(mock_world)
        assert social.world == mock_world
        print("✓ SocialSystem instantiated")
    except Exception as e:
        print(f"✗ SocialSystem failed: {e}")
        return False
        
    try:
        economy = EconomySystem(mock_world)
        assert economy.world == mock_world
        print("✓ EconomySystem instantiated")
    except Exception as e:
        print(f"✗ EconomySystem failed: {e}")
        return False
    
    print("✓ All ECS systems can be instantiated")
    return True

async def test_world_basic_functionality():
    """Test basic AgentropolisWorld functionality."""
    print("\nTesting AgentropolisWorld basic functionality...")
    
    from agentropolis.engine.world import AgentropolisWorld
    
    # Test instantiation
    world = AgentropolisWorld()
    assert world.ecs_world is not None
    assert len(world.agent_entities) == 0
    assert len(world.location_entities) == 0
    print("✓ AgentropolisWorld instantiated")
    
    # Test that we can get the ECS world
    ecs_world = world.get_world()
    assert ecs_world is world.ecs_world
    print("✓ ECS world retrieval works")
    
    print("✓ AgentropolisWorld basic functionality works")
    return True

def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("AGENTROPOLIS ECS TASK 2 VERIFICATION TESTS")
    print("=" * 60)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("ECS Core Functionality", test_ecs_core_functionality),
        ("All Component Types", test_all_component_types),
        ("Systems Instantiation", test_systems_can_be_instantiated),
        ("World Basic Functionality", lambda: asyncio.run(test_world_basic_functionality())),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"🟢 {test_name}: PASSED")
                passed += 1
            else:
                print(f"🔴 {test_name}: FAILED")
                failed += 1
        except Exception as e:
            print(f"🔴 {test_name}: ERROR - {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        print()
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed, {passed+failed} total")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! ECS Task 2 implementation is working correctly.")
        print("✅ Ready to proceed with Task 2 enhancements.")
        return True
    else:
        print("❌ SOME TESTS FAILED. Please review the implementation.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)