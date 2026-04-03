"""World management for the ECS-based simulation."""
import asyncio
import logging
import time
from typing import Dict, List, Optional
from uuid import UUID
from agentropolis.models import Agent, Location
from agentropolis.database import AsyncSessionLocal
from agentropolis.engine.ecs import World as EcsWorld, Entity
from agentropolis.engine.components import *

logger = logging.getLogger(__name__)

class AgentropolisWorld:
    """Bridge between ECS world and database-persisted models."""
    
    def __init__(self):
        self.ecs_world = EcsWorld()
        self.agent_entities: Dict[UUID, Entity] = {}  # agent_id -> entity
        self.location_entities: Dict[UUID, Entity] = {}  # location_id -> entity
        self._sync_interval = 5.0  # seconds between DB<->ECS sync
        self._last_sync = 0.0
        
    async def initialize_from_database(self):
        """Load initial state from database into ECS."""
        logger.info("Loading world state from database...")
        
        async with AsyncSessionLocal() as session:
            from sqlalchemy import select
            
            # Load all active agents
            agents_result = await session.execute(
                select(Agent).where(Agent.is_active == True)
            )
            agents = list(agents_result.scalars().all())
            
            # Load all locations
            locations_result = await session.execute(select(Location))
            locations = list(locations_result.scalars().all())
            
            # Convert agents to ECS entities
            for agent in agents:
                entity = self._agent_to_entity(agent)
                self.ecs_world.entities[entity.id] = entity
                self.agent_entities[agent.id] = entity
                logger.debug(f"Loaded agent {agent.name} as entity {entity.id}")
            
            # Convert locations to ECS entities (simplified - just position for now)
            for location in locations:
                entity = self._location_to_entity(location)
                self.ecs_world.entities[entity.id] = entity
                self.location_entities[location.id] = entity
                logger.debug(f"Loaded location {location.name} as entity {entity.id}")
            
            logger.info(f"Loaded {len(agents)} agents and {len(locations)} locations into ECS world")
    
    def _agent_to_entity(self, agent: Agent) -> Entity:
        """Convert SQLAlchemy Agent model to ECS entity with components."""
        entity = Entity(id=agent.id)
        
        # Add components
        entity.add_component(PositionComponent(x=agent.x, y=agent.y))
        entity.add_component(BodyComponent(
            health=agent.health,
            energy=agent.energy,
            hunger=agent.hunger
        ))
        entity.add_component(MindComponent(happiness=agent.happiness))
        entity.add_component(IdentityComponent(
            name=agent.name,
            agent_type=agent.type
        ))
        entity.add_component(EconomicsComponent(money=agent.money))
        entity.add_component(SocialComponent())
        entity.add_component(OccupationComponent(
            occupation=agent.occupation or "unemployed",
            employed=bool(agent.occupation)
        ))
        entity.add_component(LocationComponent(location_id=agent.location_id))
        entity.add_component(AgentStateComponent(is_active=agent.is_active))
        
        return entity
    
    def _location_to_entity(self, location: Location) -> Entity:
        """Convert SQLAlchemy Location model to ECS entity."""
        entity = Entity(id=location.id)
        
        # Locations primarily need position for spatial queries
        entity.add_component(PositionComponent(x=location.x, y=location.y))
        
        # Could add more components for location properties if needed
        # For now, we'll keep location-specific data in the SQL model
        
        return entity
    
    def _entity_to_agent_update(self, entity: Entity) -> Dict[str, any]:
        """Extract updated fields from ECS entity for database update."""
        updates = {}
        
        if entity.has_component(PositionComponent):
            pos = entity.get_component(PositionComponent)
            updates.update({
                'x': pos.x,
                'y': pos.y
            })
        
        if entity.has_component(BodyComponent):
            body = entity.get_component(BodyComponent)
            updates.update({
                'health': body.health,
                'energy': body.energy,
                'hunger': body.hunger
            })
        
        if entity.has_component(MindComponent):
            mind = entity.get_component(MindComponent)
            updates.update({
                'happiness': mind.happiness
            })
        
        if entity.has_component(EconomicsComponent):
            eco = entity.get_component(EconomicsComponent)
            updates.update({
                'money': eco.money
            })
        
        if entity.has_component(LocationComponent):
            loc = entity.get_component(LocationComponent)
            updates.update({
                'location_id': loc.location_id
            })
        
        if entity.has_component(AgentStateComponent):
            state = entity.get_component(AgentStateComponent)
            updates.update({
                'is_active': state.is_active
            })
        
        return updates
    
    async def sync_to_database(self):
        """Sync ECS entity states back to database."""
        logger.debug("Syncing ECS world to database...")
        
        async with AsyncSessionLocal() as session:
            from sqlalchemy import update
            
            # Sync agents
            for agent_id, entity in self.agent_entities.items():
                updates = self._entity_to_agent_update(entity)
                if updates:
                    await session.execute(
                        update(Agent)
                        .where(Agent.id == agent_id)
                        .values(**updates)
                    )
            
            await session.commit()
            logger.debug(f"Synced {len(self.agent_entities)} agents to database")
    
    async def sync_from_database(self):
        """Sync database state to ECS (for external changes)."""
        logger.debug("Syncing database to ECS world...")
        
        # For simplicity, we'll just reload from database
        # In a more sophisticated version, we'd diff and update only changed entities
        await self.initialize_from_database()
    
    def get_world(self):
        """Get the underlying ECS world."""
        return self.ecs_world