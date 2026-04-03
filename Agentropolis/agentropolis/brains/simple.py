"""Simple rule-based brain for agents."""
import random
from typing import Dict, Any, Optional, List
from uuid import UUID
from agentropolis.models import Agent, Location
from .base import Brain, BrainDecision

class SimpleBrain(Brain):
    """A simple brain that makes decisions based on agent needs and basic rules."""
    
    def __init__(self, agent_id: UUID):
        super().__init__(agent_id)
        # Need thresholds (0-100 scale)
        self.hunger_threshold = 70
        self.energy_threshold = 30
        self.happiness_threshold = -20
        self.health_threshold = 50
        
    async def decide(self, agent: Agent, world_state: Dict[str, Any]) -> BrainDecision:
        """Make a decision based on agent's current needs and surroundings."""
        
        # Check critical needs first (override everything else)
        if agent.hunger >= self.hunger_threshold:
            # Find food source
            food_location = self._find_nearest_service(world_state.get('locations', []), 'provides_food')
            if food_location:
                return BrainDecision(
                    action_type="move",
                    target_id=food_location.id,
                    parameters={"priority": "high"},
                    confidence=0.9,
                    reasoning=f"Hungry ({agent.hunger}), seeking food"
                )
        
        if agent.energy <= self.energy_threshold:
            # Find place to rest/sleep
            rest_location = self._find_nearest_service(world_state.get('locations', []), 'provides_sleep')
            if rest_location:
                return BrainDecision(
                    action_type="move",
                    target_id=rest_location.id,
                    parameters={"priority": "high"},
                    confidence=0.9,
                    reasoning=f"Tired ({agent.energy}), seeking rest"
                )
        
        if agent.health <= self.health_threshold:
            # Find healthcare
            health_location = self._find_nearest_service(world_state.get('locations', []), 'provides_healthcare')
            if health_location:
                return BrainDecision(
                    action_type="move",
                    target_id=health_location.id,
                    parameters={"priority": "high"},
                    confidence=0.9,
                    reasoning=f"Unhealthy ({agent.health}), seeking healthcare"
                )
        
        # Check happiness - if very unhappy, seek entertainment/social
        if agent.happiness <= self.happiness_threshold:
            # Try to find entertainment or social opportunities
            social_location = self._find_nearest_service(world_state.get('locations', []), 'provides_entertainment')
            if social_location and random.random() < 0.7:  # 70% chance to seek entertainment
                return BrainDecision(
                    action_type="move",
                    target_id=social_location.id,
                    parameters={"priority": "medium"},
                    confidence=0.7,
                    reasoning=f"Unhappy ({agent.happiness}), seeking entertainment"
                )
        
        # If we have money and basic needs are met, consider working to earn more
        if agent.money < 50 and agent.energy > 50 and agent.hunger < 50:
            work_location = self._find_nearest_service(world_state.get('locations', []), 'provides_work')
            if work_location:
                return BrainDecision(
                    action_type="work",
                    target_id=work_location.id,
                    parameters={"duration": random.randint(1, 3)},
                    confidence=0.6,
                    reasoning=f"Low money ({agent.money}), seeking work"
                )
        
        # Default: wander or socialize
        nearby_agents = [a for a in world_state.get('agents', []) if a.id != agent.id]
        if nearby_agents and random.random() < 0.3:  # 30% chance to socialize
            target_agent = random.choice(nearby_agents)
            return BrainDecision(
                action_type="socialize",
                target_id=target_agent.id,
                parameters={"topic": random.choice(["weather", "work", "family", "hobbies"])},
                confidence=0.5,
                reasoning="Feeling social"
            )
        
        # Random movement or idle
        if random.random() < 0.4:  # 40% chance to move somewhere
            locations = world_state.get('locations', [])
            if locations:
                target_location = random.choice(locations)
                return BrainDecision(
                    action_type="move",
                    target_id=target_location.id,
                    parameters={"wander": True},
                    confidence=0.4,
                    reasoning="Random movement"
                )
        
        # Default action: idle/wait
        return BrainDecision(
            action_type="idle",
            parameters={"duration": random.randint(1, 5)},
            confidence=0.3,
            reasoning="Nothing pressing to do"
        )
    
    def _find_nearest_service(self, locations: List[Location], service_attr: str) -> Optional[Location]:
        """Find the nearest location that provides a specific service."""
        if not locations:
            return None
        
        # Filter locations that provide the service
        service_locations = [
            loc for loc in locations 
            if getattr(loc, service_attr, False)
        ]
        
        if not service_locations:
            return None
        
        # For now, just return the first one (in a full implementation, 
        # we'd calculate actual distance based on x,y coordinates)
        return random.choice(service_locations)