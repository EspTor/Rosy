"""Seed initial town data.""""""
import asyncio
import uuid
from agentropolis.database import AsyncSessionLocal
from agentropolis.models import Agent, Location

async def seed():
    async with AsyncSessionLocal() as session:
        locations = [
            Location(id=uuid.uuid4(), name="Town Center", type="civic", district="downtown", x=0, y=0, capacity=50, provides_food=True, provides_entertainment=True),
            Location(id=uuid.uuid4(), name="North Housing", type="residential", district="residential_north", x=0, y=100, capacity=30, provides_sleep=True),
            Location(id=uuid.uuid4(), name="South Housing", type="residential", district="residential_south", x=0, y=-100, capacity=30, provides_sleep=True),
            Location(id=uuid.uuid4(), name="Factory District", type="workplace", district="industrial", x=150, y=0, capacity=50, provides_work=True),
            Location(id=uuid.uuid4(), name="Market Square", type="commercial", district="market", x=-100, y=0, capacity=30, provides_food=True, provides_entertainment=True),
        ]
        for loc in locations:
            session.add(loc)
        await session.commit()
        print(f"Created {len(locations)} locations")
        
        agents = [
            Agent(name="Alice", type="worker", occupation="factory_worker", location_id=locations[1].id, x=0, y=100, money=150.0, is_llm_enabled=False),
            Agent(name="Bob", type="worker", occupation="factory_worker", location_id=locations[2].id, x=0, y=-100, money=120.0, is_llm_enabled=False),
            Agent(name="Charlie", type="socialite", occupation="none", location_id=locations[0].id, x=0, y=0, money=200.0, is_llm_enabled=True),
            Agent(name="Diana", type="worker", occupation="shopkeeper", location_id=locations[4].id, x=-100, y=0, money=500.0, is_llm_enabled=False),
            Agent(name="Eve", type="worker", occupation="factory_worker", location_id=locations[1].id, x=5, y=105, money=80.0, is_llm_enabled=False),
        ]
        for agent in agents:
            session.add(agent)
        await session.commit()
        print(f"Created {len(agents)} agents")
        
        for loc in locations:
            loc.current_occupancy = sum(1 for a in agents if a.location_id == loc.id)
            session.add(loc)
        await session.commit()
        print("Updated occupancy")

if __name__ == "__main__":
    asyncio.run(seed())
