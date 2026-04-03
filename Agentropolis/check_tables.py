import asyncio
from agentropolis.database import async_engine
from sqlalchemy import text

async def check_tables():
    async with async_engine.begin() as conn:
        result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = result.fetchall()
        print('Tables:', [t[0] for t in tables])

if __name__ == "__main__":
    asyncio.run(check_tables())