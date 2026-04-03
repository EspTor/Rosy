"""Seed initial town data."""
import asyncio
import uuid
from agentropolis.database import AsyncSessionLocal
from agentropolis.models import Agent, Location

async def seed():
    """Create initial agents and locations for the town."""
    async with AsyncSessionLocal() as session:
        # Create 5 locations with various services
        locations = [
            Location(
                name="Town Center",
                type="civic",
                district="downtown",
                x=0,
                y=0,
                capacity=50,
                provides_food=True,
                provides_entertainment=True,
                provides_work=True
            ),
            Location(
                name="North Housing",
                type="residential",
                district="residential_north",
                x=0,
                y=100,
                capacity=30,
                provides_sleep=True
            ),
            Location(
                name="South Housing",
                type="residential",
                district="residential_south",
                x=0,
                y=-100,
                capacity=30,
                provides_sleep=True
            ),
            Location(
                name="Factory District",
                type="workplace",
                district="industrial",
                x=150,
                y=0,
                capacity=50,
                provides_work=True
            ),
            Location(
                name="Market Square",
                type="commercial",
                district="market",
                x=-100,
                y=0,
                capacity=30,
                provides_food=True,
                provides_entertainment=True
            ),
        ]
        for loc in locations:
            session.add(loc)
        await session.commit()
        print(f"Created {len(locations)} locations")

        # Create 5 agents with varied types and assignments
        agents = []
        town_center = locations[0]
        north_housing = locations[1]
        south_housing = locations[2]
        factory = locations[3]
        market = locations[4]

        # Alice: worker at factory, lives north (closer to housing)
        alice = Agent(
            name="Alice",
            type="worker",
            occupation="factory_worker",
            location_id=town_center.id,
            x=10,
            y=10,
            health=90,
            energy=80,
            hunger=30,
            happiness=70,
            money=1000.0
        )
        agents.append(alice)
        town_center.current_occupancy += 1

        # Bob: worker at market, lives south
        bob = Agent(
            name="Bob",
            type="worker",
            occupation="shop_keeper",
            location_id=market.id,
            x=-90,
            y=10,
            health=85,
            energy=70,
            hunger=50,
            happiness=60,
            money=800.0
        )
        agents.append(bob)
        market.current_occupancy += 1

        # Carol: retired, stays at town center
        carol = Agent(
            name="Carol",
            type="retired",
            occupation="elder",
            location_id=town_center.id,
            x=5,
            y=5,
            health=70,
            energy=60,
            hunger=40,
            happiness=80,
            money=500.0
        )
        agents.append(carol)
        town_center.current_occupancy += 1

        # David: student, near north housing
        david = Agent(
            name="David",
            type="student",
            occupation="pupil",
            location_id=north_housing.id,
            x=10,
            y=110,
            health=95,
            energy=90,
            hunger=20,
            happiness=90,
            money=200.0
        )
        agents.append(david)
        north_housing.current_occupancy += 1

        # Eve: entrepreneur, based in market
        eve = Agent(
            name="Eve",
            type="entrepreneur",
            occupation="business_owner",
            location_id=market.id,
            x=-110,
            y=10,
            health=88,
            energy=75,
            hunger=40,
            happiness=75,
            money=1500.0
        )
        agents.append(eve)
        market.current_occupancy += 1

        for agent in agents:
            session.add(agent)
        # Locations have been modified (occupancy) and are still attached; they will be updated
        await session.commit()
        print(f"Created {len(agents)} agents")

if __name__ == "__main__":
    asyncio.run(seed())
