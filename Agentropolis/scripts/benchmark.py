"""Performance benchmarks for Agentropolis."""
import asyncio
import time
from agentropolis.database import AsyncSessionLocal, init_db, close_db
from agentropolis.models import Agent, Location

async def benchmark_agent_insert(num_agents: int = 1000):
    """Benchmark inserting many agents."""
    await init_db()
    async with AsyncSessionLocal() as session:
        start = time.time()
        for i in range(num_agents):
            agent = Agent(
                name=f"Agent{i}",
                type="benchmark",
                x=0.0,
                y=0.0
            )
            session.add(agent)
        await session.commit()
        elapsed = time.time() - start
        print(f"Inserted {num_agents} agents in {elapsed:.3f}s ({num_agents/elapsed:.1f} agents/s)")
        assert elapsed < 5.0, f"Too slow: {elapsed:.3f}s (target: <5s)"
    await close_db()

async def benchmark_location_query():
    """Benchmark location lookup."""
    await init_db()
    # Insert a test location
    async with AsyncSessionLocal() as session:
        loc = Location(name="BenchLoc", type="test", district="test", x=0.0, y=0.0)
        session.add(loc)
        await session.commit()
        loc_id = loc.id

    # Benchmark query
    async with AsyncSessionLocal() as session:
        start = time.time()
        for _ in range(100):
            result = await session.get(Location, loc_id)
        elapsed = time.time() - start
        avg = elapsed / 100
        print(f"Location query avg: {avg*1000:.3f}ms (target: <100ms)")
        assert avg < 0.1, f"Query too slow: {avg*1000:.3f}ms (target: <100ms)"
    await close_db()

async def benchmark_relationship_query():
    """Benchmark relationship lookup."""
    await init_db()
    async with AsyncSessionLocal() as session:
        # Create agents and relationship
        a = Agent(name="RelA", type="test")
        b = Agent(name="RelB", type="test")
        session.add_all([a, b])
        await session.commit()

        rel = Relationship(agent_a_id=a.id, agent_b_id=b.id, type="test")
        session.add(rel)
        await session.commit()

        # Benchmark query
        start = time.time()
        for _ in range(100):
            result = await session.get(Relationship, (a.id, b.id))
        elapsed = time.time() - start
        avg = elapsed / 100
        print(f"Relationship query avg: {avg*1000:.3f}ms (target: <100ms)")
        assert avg < 0.1, f"Query too slow: {avg*1000:.3f}ms (target: <100ms)"
    await close_db()

async def main():
    print("Running performance benchmarks...")
    print("-" * 50)
    await benchmark_agent_insert()
    await benchmark_location_query()
    await benchmark_relationship_query()
    print("-" * 50)
    print("✅ All benchmarks passed!")

if __name__ == "__main__":
    # Import Relationship for the relationship benchmark
    from agentropolis.models import Relationship
    asyncio.run(main())
