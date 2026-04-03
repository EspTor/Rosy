import asyncio
from agentropolis.database import Base, async_engine
from agentropolis.models import Agent, Location  # Force import
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def debug_init():
    print("Base metadata tables before:", list(Base.metadata.tables.keys()))
    print("Agent table:", Agent.__tablename__ if hasattr(Agent, '__tablename__') else 'No tablename')
    print("Location table:", Location.__tablename__ if hasattr(Location, '__tablename__') else 'No tablename')
    
    async with async_engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created.")
    
    # Check what tables exist now
    print("Base metadata tables after:", list(Base.metadata.tables.keys()))
    
    async with async_engine.begin() as conn:
        from sqlalchemy import text
        result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = result.fetchall()
        print('Actual DB tables:', [t[0] for t in tables])

if __name__ == "__main__":
    asyncio.run(debug_init())