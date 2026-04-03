"""Database connection and table creation tests."""
import pytest
from sqlalchemy import text
from agentropolis.database import async_engine

@pytest.mark.asyncio
async def test_connection():
    """Test that we can connect to the database."""
    async with async_engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
    print("✓ Database connection OK")

@pytest.mark.asyncio
async def test_create_tables(db_session):
    """Test that tables can be created (via db_session fixture)."""
    # Use the db_session to check tables; it already created them.
    result = await db_session.execute(
        text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    )
    tables = [row[0] for row in result.fetchall()]
    assert 'agents' in tables
    assert 'locations' in tables
    assert 'relationships' in tables
    print("✓ All tables exist")

if __name__ == "__main__":
    import pytest as pt
    pt.main([__file__, "-v"])
