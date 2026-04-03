"""ECS components for Agentropolis - bridges ECS with existing SQLAlchemy models."""
import uuid
from typing import Optional, List
from agentropolis.models import Agent as SqlAgent, Location as SqlLocation
from agentropolis.models.relationship import Relationship

class PositionComponent:
    """Position in the 2D world."""
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

class BodyComponent:
    """Physical body of an agent."""
    def __init__(self, health: int = 100, energy: int = 100, hunger: int = 0):
        self.health = health
        self.energy = energy
        self.hunger = hunger

class MindComponent:
    """Mental state of an agent."""
    def __init__(self, happiness: int = 25):
        self.happiness = happiness

class IdentityComponent:
    """Who the agent is."""
    def __init__(self, name: str = "Unknown", agent_type: str = "citizen"):
        self.name = name
        self.agent_type = agent_type

class EconomicsComponent:
    """Financial state."""
    def __init__(self, money: float = 100.0):
        self.money = money

class SocialComponent:
    """Social relationships and interactions."""
    def __init__(self):
        self.relationships: List[uuid.UUID] = []  # IDs of related agents
        self.last_social_tick: int = 0

class OccupationComponent:
    """Job and employment info."""
    def __init__(self, occupation: str = "unemployed", employed: bool = False):
        self.occupation = occupation
        self.employed = employed

class LocationComponent:
    """Current location of the agent."""
    def __init__(self, location_id: Optional[uuid.UUID] = None):
        self.location_id = location_id

class AgentStateComponent:
    """Current state flags."""
    def __init__(self, is_active: bool = True, is_sleeping: bool = False):
        self.is_active = is_active
        self.is_sleeping = is_sleeping