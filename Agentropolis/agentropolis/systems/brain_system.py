"""System for managing agent brains and decision-making."""
import asyncio
import logging
from typing import Dict, List, Optional, Set, Type, Union
from uuid import UUID
from agentropolis.models import Agent, Location
from agentropolis.database import AsyncSessionLocal
from agentropolis.brains import SimpleBrain, LLMBrain
from agentropolis.brains.base import Brain

logger = logging.getLogger(__name__)

class BrainSystem:
    """Manages the creation and updating of agent brains."""
    
    def __init__(self):
        self.brains: Dict[UUID, Brain] = {}  # agent_id -> brain
        self._default_brain_class: Type[SimpleBrain] = SimpleBrain
        self._llm_agent_ids: Set[str] = set()  # agent IDs that get LLM brains
        
    def register_llm_agents(self, agent_ids: Set[str]):
        """Mark specific agents to use LLM brains instead of rule-based."""
        self._llm_agent_ids = agent_ids
        # Update existing brains if any already created
        for aid, brain in list(self.brains.items()):
            if str(aid) in agent_ids:
                self.clear_brain(aid)  # Will be recreated as LLM on next get
                logger.debug(f"Converted agent {aid} to LLM brain")
        
    def get_brain(self, agent_id: UUID) -> Brain:
        """Get or create a brain for an agent."""
        if agent_id not in self.brains:
            use_llm = str(agent_id) in self._llm_agent_ids
            brain_class = LLMBrain if use_llm else self._default_brain_class
            self.brains[agent_id] = brain_class(agent_id)
            logger.debug(
                f"Created {'LLM' if use_llm else 'Simple'} brain for agent {agent_id}"
            )
        return self.brains[agent_id]
    
    async def make_decision(
        self, 
        agent: Agent, 
        world_state: Dict[str, any]
    ) -> Optional[Dict[str, any]]:
        """
        Make a decision for an agent based on its brain and current state.
        
        Returns:
            Dictionary representing the action to take, or None if no decision
        """
        try:
            brain = self.get_brain(agent.id)
            decision = await brain.decide(agent, world_state)
            
            # Log the decision for debugging
            logger.debug(
                f"Agent {agent.name} ({agent.id}) decided: {decision.action_type} "
                f"- {decision.reasoning}"
            )
            
            # Convert BrainDecision to action dictionary
            return {
                "agent_id": str(agent.id),
                "action_type": decision.action_type,
                "target_id": str(decision.target_id) if decision.target_id else None,
                "parameters": decision.parameters,
                "confidence": decision.confidence,
                "reasoning": decision.reasoning
            }
        except Exception as e:
            logger.error(f"Error making decision for agent {agent.id}: {e}")
            return None
    
    async def process_agents(
        self, 
        agents: List[Agent], 
        locations: List[Location]
    ) -> List[Dict[str, any]]:
        """
        Process a list of agents and generate decisions for each.
        
        Returns:
            List of action dictionaries
        """
        # Build world state
        world_state = {
            "agents": agents,
            "locations": locations,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Process each agent
        decisions = []
        for agent in agents:
            if not agent.is_active:
                continue
                
            decision = await self.make_decision(agent, world_state)
            if decision:
                decisions.append(decision)
        
        return decisions
    
    def clear_brain(self, agent_id: UUID):
        """Remove an agent's brain (e.g., when agent dies or leaves)."""
        if agent_id in self.brains:
            del self.brains[agent_id]
            logger.debug(f"Cleared brain for agent {agent_id}")
    
    def get_brain_count(self) -> int:
        """Get the number of active brains."""
        return len(self.brains)