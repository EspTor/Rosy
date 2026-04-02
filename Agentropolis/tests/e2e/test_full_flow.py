"""End-to-end test of complete data flow.""""""
import asyncio
import uuid
import pytest
from agentropolis.database import async_engine, Base, AsyncSessionLocal, init_db, close_db
from agentropolis.models import Agent, Location
from agentropolis.config import config

@pytest.mark.asyncio
async def test_full_pipeline():
    """Test: create tables → seed town → query agents → verify integrity → cleanup."""
    
    # 1. Create fresh tables
    await init_db()
    print("✓ Database tables created")
    
    # 2. Run seed script inline (not as subprocess)
    from scripts.seed_town import seed
    await seed()
    print("✓ Seed data loaded")
    
    # 3. Verify agents exist
    async with AsyncSessionLocal() as session:
        agent_count = await session.execute("SELECT COUNT(*) FROM agents")
        count = agent_count.scalar()
        assert count == 5, f"Expected 5 agents, got {count}"
        print(f"✓ Agent count correct: {count}")
        
        # 4. Verify locations exist
        loc_count = await session.execute("SELECT COUNT(*) FROM locations")
        count = loc_count.scalar()
        assert count == 5, f"Expected 5 locations, got {count}"
        print(f"✓ Location count correct: {count}")
        
        # 5. Query specific agent (Alice)
        alice = await session.get(Agent, uuid.UUID("00000000-0000-0000-0000-000000000001"))  # But UUIDs are random!
        # Instead, query by name
        from sqlalchemy import select
        result = await session.execute(select(Agent).where(Agent.name == "Alice"))
        alice = result.scalar_one_or_none()
        assert alice is not None, "Alice not found"
        assert alice.type == "worker"
        assert alice.money > 0
        print(f"✓ Alice found: type={alice.type}, money={alice.money}")
        
        # 6. Verify spatial query works (agents near location)
        town_center = await session.execute(select(Location).where(Location.name == "Town Center"))
        tc = town_center.scalar_one()
        assert tc.current_occupancy >= 1, "Town Center should have at least 1 occupant"
        print(f"✓ Town Center occupancy: {tc.current_occupancy}")
        
        # 7. Verify relationship tables exist (empty at this stage)
        rel_count = await session.execute("SELECT COUNT(*) FROM relationships")
        count = rel_count.scalar()
        assert count == 0, f"Expected 0 relationships initially, got {count}"
        print("✓ Relationship table empty (as expected)")
        
        # 8. Test agent movement update
        alice.x = 10.0
        alice.y = 110.0
        await session.commit()
        alice_refreshed = await session.get(Agent, alice.id)
        assert alice_refreshed.x == 10.0
        assert alice_refreshed.y == 110.0
        print("✓ Agent movement updates work")
        
        # 9. Test money transaction
        bob = await session.execute(select(Agent).where(Agent.name == "Bob"))
        bob = bob.scalar_one()
        initial_money = bob.money
        bob.money -= 10.0
        await session.commit()
        bob_refreshed = await session.get(Agent, bob.id)
        assert bob_refreshed.money == initial_money - 10.0
        print(f"✓ Money transactions work: {initial_money} -> {bob_refreshed.money}")
        
    # 10. Cleanup
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("✓ Cleanup complete")
    
    print("
✅ ALL E2E TESTS PASSED")

if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
