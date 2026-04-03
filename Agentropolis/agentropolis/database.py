"""Database connection and models using SQLAlchemy async."""
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from .config import config

# Async engine for production (using NullPool for test compatibility)
async_engine: AsyncEngine = create_async_engine(
    config.database_url,
    echo=False,
    poolclass=NullPool,
    future=True,
)

# Sync engine for migrations/scripts (if needed)
sync_engine = create_engine(
    config.database_url.replace("+asyncpg", ""),
    echo=False,
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base for ORM models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency for FastAPI or other frameworks."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create all tables (for initial setup only)."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connections on shutdown."""
    await async_engine.dispose()


def test_connection():
    """Quick test of DB connection (synchronous for scripts)."""
    try:
        conn = sync_engine.connect()
        conn.execute("SELECT 1")
        conn.close()
        print("✓ Database connection OK")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False