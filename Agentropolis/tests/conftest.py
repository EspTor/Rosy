"""Test fixtures."""
import asyncio
import pytest
import pytest_asyncio
from sqlalchemy import text
from agentropolis.database import async_engine, Base, AsyncSessionLocal

@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    """Create tables once for the entire test session."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup: drop all tables after session
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(autouse=True)
async def truncate_tables():
    """Ensure tables are empty before each test."""
    # First ensure tables exist (in case setup_db hasn't run yet in this context)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Then truncate them
    async with async_engine.begin() as conn:
        await conn.execute(
            text("TRUNCATE TABLE relationships, agents, locations RESTART IDENTITY CASCADE")
        )
    yield
    # No teardown needed

@pytest_asyncio.fixture
async def db_session():
    """Provide a fresh database session."""
    async with AsyncSessionLocal() as session:
        yield session

@pytest.fixture
def sample_agent_data():
    return {"name": "Test", "type": "worker", "x": 0.0, "y": 0.0}

@pytest.fixture
def sample_location_data():
    return {"name": "Loc", "type": "home", "district": "test", "x": 0, "y": 0}