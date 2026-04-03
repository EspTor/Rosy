"""Abstract base class for agent brains."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from agentropolis.models import Agent, Location
import uuid

@dataclass
class BrainDecision:
    """Represents a decision made by an agent's brain."""
    action_type: str  # e.g., "move", "work", "eat", "sleep", "socialize"
    target_id: Optional[uuid.UUID] = None  # Target location or agent ID
    parameters: Dict[str, Any] = None
    confidence: float = 1.0  # How confident the brain is in this decision (0.0 to 1.0)
    reasoning: str = ""  # Explanation for the decision

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}

class Brain(ABC):
    """Abstract base class for agent decision-making brains."""
    
    def __init__(self, agent_id: uuid.UUID):
        self.agent_id = agent_id
        self.memory: List[Dict[str, Any]] = []  # Short-term memory of recent events
        self.long_term_memory: Dict[str, Any] = {}  # Persistent knowledge
        
    @abstractmethod
    async def decide(self, agent: Agent, world_state: Dict[str, Any]) -> BrainDecision:
        """
        Make a decision based on the agent's current state and world state.
        
        Args:
            agent: The agent whose brain this is
            world_state: Dictionary containing relevant world information
                        (nearby agents, locations, time, resources, etc.)
        
        Returns:
            BrainDecision: The decided action
        """
        pass
    
    def remember(self, event: Dict[str, Any]):
        """Add an event to short-term memory."""
        self.memory.append(event)
        # Keep only last 100 events to prevent memory bloat
        if len(self.memory) > 100:
            self.memory.pop(0)
    
    def learn(self, key: str, value: Any):
        """Store information in long-term memory."""
        self.long_term_memory[key] = value
    
    def recall(self, key: str, default: Any = None) -> Any:
        """Retrieve information from long-term memory."""
        return self.long_term_memory.get(key, default)