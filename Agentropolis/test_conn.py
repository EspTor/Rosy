#!/usr/bin/env python3
from agentropolis.config import config
print("DATABASE_URL:", config.database_url)
from agentropolis.database import async_engine
from sqlalchemy import text
import asyncio

async def test():
    async with async_engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        print("DB OK:", result.scalar())
    await async_engine.dispose()

asyncio.run(test())
