"""End-to-end test of complete data flow."""
import asyncio
import pytest
from sqlalchemy import text
from agentropolis.database import async_engine, init_db
from agentropolis.models import Agent, Location

@pytest.mark.asyncio
async def test_full_pipeline():
    """Test: create tables → seed town → query agents → verify integrity."""
    # Ensure tables exist (init_db)
    await init_db()

    # Seed the town
    from scripts.seed_town import seed
    await seed()

    # Verify agents exist
    async with async_engine.connect() as conn:
        result = await conn.execute(text("SELECT COUNT(*) FROM agents"))
        count = result.scalar()
        assert count == 5, f"Expected 5 agents, got {count}"

        # Verify locations exist
        result = await conn.execute(text("SELECT COUNT(*) FROM locations"))
        count = result.scalar()
        assert count == 5, f"Expected 5 locations, got {count}"

        # Query specific agent (Alice)
        result = await conn.execute(
            text("SELECT name, type, money FROM agents WHERE name = 'Alice'")
        )
        row = result.first()
        assert row is not None, "Alice not found"
        assert row.type == "worker"
        assert row.money > 0

        # Verify Town Center occupancy
        result = await conn.execute(
            text("SELECT current_occupancy FROM locations WHERE name = 'Town Center'")
        )
        occ = result.scalar()
        assert occ >= 1, "Town Center should have at least 1 occupant"

    # No cleanup needed; autouse truncation will handle it.

if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
