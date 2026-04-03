#!/usr/bin/env python3
"""Basic test for ECS functionality."""
import sys
import asyncio

def test_ecs_core():
    """Test basic ECS functionality."""
    print("Testing ECS core...")
    
    # Add project to path
    sys.path.insert(0, '/home/ubuntu/Documents/Obsidian Vault/Agentropolis')
    
    from agentropolis.engine.ecs import Entity, Component
    from agentropolis.engine.components import PositionComponent, IdentityComponent
    
    # Create test entity
    entity = Entity()
    print(f"✓ Created entity: {entity.id}")
    
    # Add components
    pos = PositionComponent(x=10.0, y=20.0)
    entity.add_component(pos)
    print(f"✓ Added PositionComponent: ({pos.x}, {pos.y})")
    
    identity = IdentityComponent(name="TestAgent", agent_type="test")
    entity.add_component(identity)
    print(f"✓ Added IdentityComponent: {identity.name} ({identity.agent_type})")
    
    # Retrieve components
    retrieved_pos = entity.get_component(PositionComponent)
    retrieved_identity = entity.get_component(IdentityComponent)
    
    assert retrieved_pos is not None, "PositionComponent not found"
    assert retrieved_identity is not None, "IdentityComponent not found"
    assert retrieved_pos.x == 10.0 and retrieved_pos.y == 20.0, "Position values incorrect"
    assert retrieved_identity.name == "TestAgent", "Identity name incorrect"
    assert retrieved_identity.agent_type == "test", "Identity type incorrect"
    
    print("✓ Component retrieval works correctly")
    print("✓ ECS core test passed")
    return True

async def test_ecs_world():
    """Test ECS world initialization."""
    print("\nTesting ECS world initialization...")
    
    from agentropolis.engine.world import AgentropolisWorld
    from agentropolis.engine.components import IdentityComponent
    
    world = AgentropolisWorld()
    await world.initialize_from_database()
    
    agent_count = len(world.agent_entities)
    location_count = len(world.location_entities)
    print(f"✓ Loaded {agent_count} agents and {location_count} locations")
    
    ecs_world = world.get_world()
    print(f"✓ ECS world has {len(ecs_world.entities)} entities")
    
    # Test one agent if available
    if world.agent_entities:
        agent_id, entity = list(world.agent_entities.items())[0]
        identity_comp = entity.get_component(IdentityComponent)
        if identity_comp:
            print(f"✓ Sample agent: {identity_comp.name} ({identity_comp.agent_type})")
        else:
            print("? Sample agent has no IdentityComponent")
    
    print("✓ ECS world test passed")
    return True

def test_ecs_systems_import():
    """Test that ECS systems can be imported."""
    print("\nTesting ECS systems import...")
    
    from agentropolis.engine.systems import (
        MovementSystem, EcsBrainSystem, NeedsSystem, SocialSystem, EconomySystem
    )
    
    print("✓ All ECS systems imported successfully")
    return True

def test_engine_package():
    """Test the engine package as a whole."""
    print("\nTesting engine package...")
    
    from agentropolis.engine import World, Entity as EngineEntity, Component as EngineComponent
    from agentropolis.engine.systems import MovementSystem, EcsBrainSystem
    
    print("✓ Engine package imports work correctly")
    return True

async def main():
    """Run all tests."""
    print("=" * 50)
    print("Agentropolis ECS Basic Tests")
    print("=" * 50)
    
    try:
        test_ecs_core()
        await test_ecs_world()
        test_ecs_systems_import()
        test_engine_package()
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("ECS foundation is working correctly.")
        print("=" * 50)
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)