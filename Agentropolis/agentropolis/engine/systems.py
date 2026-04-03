"""ECS systems for Agentropolis simulation."""
import asyncio
import logging
import math
import random
from typing import Dict, List, Optional, Tuple
from uuid import UUID
from agentropolis.engine.ecs import System, Entity
from agentropolis.engine.components import *
from agentropolis.models import Agent, Location
from agentropolis.database import AsyncSessionLocal

logger = logging.getLogger(__name__)

class MovementSystem(System):
    """Handles agent movement based on intentions and pathfinding."""
    
    def __init__(self, world):
        super().__init__(world)
        self.required_components = {PositionComponent}
        # Simple movement speed: units per second
        self.movement_speed = 2.0
    
    async def process(self, entities: Dict[UUID, Entity], delta_time: float):
        """Process movement for all entities with movement intentions."""
        # In a full implementation, we'd read movement intentions from a component
        # For now, we'll simulate random wandering for demo purposes
        
        for entity_id, entity in entities.items():
            if not entity.has_component(PositionComponent):
                continue
                
            # Simple random walk for demonstration
            # In reality, this would be driven by brain decisions
            pos = entity.get_component(PositionComponent)
            
            # Random movement with small probability
            if random.random() < 0.1:  # 10% chance to move each tick
                # Move in random direction
                angle = random.uniform(0, 2 * math.pi)
                distance = self.movement_speed * delta_time
                pos.x += math.cos(angle) * distance
                pos.y += math.sin(angle) * distance
                
                logger.debug(f"Entity {entity_id} moved to ({pos.x:.2f}, {pos.y:.2f})")

class EcsBrainSystem(System):
    """ECS wrapper for agent decision-making brains."""
    
    def __init__(self, world):
        super().__init__(world)
        self.required_components = {
            PositionComponent, BodyComponent, MindComponent, 
            IdentityComponent, EconomicsComponent
        }
        # Import the brain system from earlier implementation
        from agentropolis.systems.brain_system import BrainSystem
        self.brain_system = BrainSystem()
        
        # Cache for locations to avoid DB queries every tick
        self._locations_cache: Dict[UUID, Location] = {}
        self._locations_cache_time = 0
        self._cache_ttl = 5.0  # seconds
    
    async def _get_locations(self) -> List[Location]:
        """Get locations from database with caching."""
        import time
        now = time.time()
        
        if (now - self._locations_cache_time) > self._cache_ttl or not self._locations_cache:
            async with AsyncSessionLocal() as session:
                from sqlalchemy import select
                result = await session.execute(select(Location))
                self._locations_cache = {loc.id: loc for loc in result.scalars().all()}
                self._locations_cache_time = now
                logger.debug(f"Refreshed location cache: {len(self._locations_cache)} locations")
        
        return list(self._locations_cache.values())
    
    async def process(self, entities: Dict[UUID, Entity], delta_time: float):
        """Process brain decisions for all agents."""
        # Get current locations for spatial queries
        locations = await self._get_locations()
        
        for entity_id, entity in entities.items():
            if not all(entity.has_component(comp) for comp in self.required_components):
                continue
            
            # Convert ECS entity back to agent-like object for brain system
            agent_proxy = self._entity_to_agent_proxy(entity)
            
            # Build world state
            world_state = {
                "agents": [self._entity_to_agent_proxy(e) for e in entities.values() 
                          if e.has_component(PositionComponent)],
                "locations": locations
            }
            
            # Get decision from brain system
            decision = await self.brain_system.make_decision(agent_proxy, world_state)
            
            if decision:
                # Apply decision to entity components
                await self._apply_decision(entity, decision, delta_time)
    
    def _entity_to_agent_proxy(self, entity: Entity):
        """Create a proxy object that mimics Agent for the brain system."""
        class AgentProxy:
            def __init__(self, e):
                self.id = e.id
                self.name = e.get_component(IdentityComponent).name if e.has_component(IdentityComponent) else "Unknown"
                self.type = e.get_component(IdentityComponent).agent_type if e.has_component(IdentityComponent) else "citizen"
                self.health = e.get_component(BodyComponent).health if e.has_component(BodyComponent) else 100
                self.energy = e.get_component(BodyComponent).energy if e.has_component(BodyComponent) else 100
                self.hunger = e.get_component(BodyComponent).hunger if e.has_component(BodyComponent) else 0
                self.happiness = e.get_component(MindComponent).happiness if e.has_component(MindComponent) else 25
                self.money = e.get_component(EconomicsComponent).money if e.has_component(EconomicsComponent) else 100.0
                self.x = e.get_component(PositionComponent).x if e.has_component(PositionComponent) else 0.0
                self.y = e.get_component(PositionComponent).y if e.has_component(PositionComponent) else 0.0
                self.location_id = e.get_component(LocationComponent).location_id if e.has_component(LocationComponent) else None
                self.occupation = e.get_component(OccupationComponent).occupation if e.has_component(OccupationComponent) else "unemployed"
                self.is_active = True  # Assume active if in ECS world
        
        return AgentProxy(entity)
    
    async def _apply_decision(self, entity: Entity, decision: dict, delta_time: float):
        """Apply a brain decision to update entity components."""
        action_type = decision.get("action_type")
        target_id = decision.get("target_id")
        params = decision.get("parameters", {})
        
        if action_type == "move" and target_id:
            # Move towards target location
            await self._handle_movement(entity, target_id, params, delta_time)
        elif action_type == "work":
            await self._handle_work(entity, params)
        elif action_type == "socialize":
            await self._handle_socialize(entity, target_id, params)
        elif action_type == "idle":
            await self._handle_idle(entity, params)
        # Add more action types as needed
    
    async def _handle_movement(self, entity: Entity, target_id: str, params: dict, delta_time: float):
        """Handle movement decision."""
        if not target_id:
            return
            
        try:
            target_uuid = UUID(target_id)
            # In a full implementation, we'd pathfind to the target
            # For now, simple movement toward target
            pos = entity.get_component(PositionComponent)
            
            # Get target position (would need location entity lookup)
            # Simplified: just wander a bit
            if random.random() < 0.3:
                angle = random.uniform(0, 2 * math.pi)
                distance = 1.0 * delta_time
                pos.x += math.cos(angle) * distance
                pos.y += math.sin(angle) * distance
                
                # Energy cost
                body = entity.get_component(BodyComponent)
                body.energy = max(0, body.energy - int(distance * 2))
        except ValueError:
            logger.warning(f"Invalid target ID for movement: {target_id}")
    
    async def _handle_work(self, entity: Entity, params: dict):
        """Handle work decision."""
        duration = params.get("duration", 1)
        money_earned = duration * 8  # Slightly less than before for balance
        energy_cost = duration * 4
        hunger_increase = duration * 2
        
        if entity.has_component(EconomicsComponent):
            eco = entity.get_component(EconomicsComponent)
            eco.money += money_earned
        
        if entity.has_component(BodyComponent):
            body = entity.get_component(BodyComponent)
            body.energy = max(0, body.energy - energy_cost)
            body.hunger = min(100, body.hunger + hunger_increase)
    
    async def _handle_socialize(self, entity: Entity, target_id: str, params: dict):
        """Handle socialize decision."""
        if not target_id:
            return
            
        try:
            target_uuid = UUID(target_id)
            # In full implementation, we'd find the target agent entity
            # For now, just give happiness boost
            happiness_gain = 3
            
            if entity.has_component(MindComponent):
                mind = entity.get_component(MindComponent)
                mind.happiness = min(100, mind.happiness + happiness_gain)
            
            # Small energy cost
            if entity.has_component(BodyComponent):
                body = entity.get_component(BodyComponent)
                body.energy = max(0, body.energy - 1)
        except ValueError:
            logger.warning(f"Invalid target ID for socialize: {target_id}")
    
    async def _handle_idle(self, entity: Entity, params: dict):
        """Handle idle decision."""
        duration = params.get("duration", 1)
        
        # Slow regeneration when idle
        if entity.has_component(BodyComponent):
            body = entity.get_component(BodyComponent)
            body.energy = min(100, body.energy + duration)
            body.hunger = min(100, body.hunger + duration // 2)
        
        # Happiness drifts toward neutral
        if entity.has_component(MindComponent):
            mind = entity.get_component(MindComponent)
            if mind.happiness > 0:
                mind.happiness = max(0, mind.happiness - 1)
            elif mind.happiness < 0:
                mind.happiness = min(0, mind.happiness + 1)

class NeedsSystem(System):
    """Handles natural decay and regeneration of agent needs."""
    
    def __init__(self, world):
        super().__init__(world)
        self.required_components = {BodyComponent, MindComponent}
    
    async def process(self, entities: Dict[UUID, Entity], delta_time: float):
        """Apply natural needs changes over time."""
        for entity_id, entity in entities.items():
            if not all(entity.has_component(comp) for comp in self.required_components):
                continue
            
            body = entity.get_component(BodyComponent)
            mind = entity.get_component(MindComponent)
            
            # Hunger increases slowly
            body.hunger = min(100, body.hunger + delta_time * 0.5)
            
            # Energy decreases slowly (unless being replenished)
            body.energy = max(0, body.energy - delta_time * 0.3)
            
            # Happiness drifts toward neutral (0)
            if mind.happiness > 0:
                mind.happiness = max(0, mind.happiness - delta_time * 0.2)
            elif mind.happiness < 0:
                mind.happiness = min(0, mind.happiness + delta_time * 0.2)
            
            # Health effects from extreme needs
            if body.hunger > 90:
                body.health = max(0, body.health - delta_time * 1.0)
            elif body.hunger > 70:
                body.health = max(0, body.health - delta_time * 0.5)
            
            if body.energy < 10:
                body.health = max(0, body.health - delta_time * 0.5)

class SocialSystem(System):
    """Handles social interactions and relationship updates."""
    
    def __init__(self, world):
        super().__init__(world)
        self.required_components = {SocialComponent}
    
    async def process(self, entities: Dict[UUID, Entity], delta_time: float):
        """Process social dynamics."""
        # Decay relationship strength over time
        for entity_id, entity in entities.items():
            if not entity.has_component(SocialComponent):
                continue
            
            social = entity.get_component(SocialComponent)
            # In a full implementation, we'd decay relationship strengths
            # For now, just track last social interaction time
            social.last_social_tick += delta_time

class EconomySystem(System):
    """Handles economic transactions and market dynamics."""
    
    def __init__(self, world):
        super().__init__(world)
        self.required_components = {EconomicsComponent}
    
    async def process(self, entities: Dict[UUID, Entity], delta_time: float):
        """Process economic interactions."""
        # For now, just handle passive income/expenses
        # In a full implementation, we'd handle transactions, markets, etc.
        for entity_id, entity in entities.items():
            if not entity.has_component(EconomicsComponent):
                continue
            
            eco = entity.get_component(EconomicsComponent)
            
            # Small passive income (like investments or benefits)
            if eco.money < 1000:  # Cap to prevent infinite growth
                eco.money += delta_time * 0.1  # 0.1 money per second