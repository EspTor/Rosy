"""Create database tables.""""""

import asyncio
from agentropolis.database import async_engine, init_db

async def create():
    print("Creating database tables...")
    await init_db()
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create())
