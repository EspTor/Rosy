"""Test fixtures.""""""
import asyncio
import pytest
import pytest_asyncio
from agentropolis.database import async_engine, Base, AsyncSessionLocal

@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def sample_agent_data():
    return {"name": "Test", "type": "worker", "x": 0.0, "y": 0.0}

@pytest.fixture
def sample_location_data():
    return {"name": "Loc", "type": "home", "district": "test", "x": 0, "y": 0}
