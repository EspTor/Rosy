"""Main simulation loop for Agentropolis."""
import asyncio
import logging
import os
import random
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
from agentropolis.models import Agent, Location
from agentropolis.database import AsyncSessionLocal
from agentropolis.systems.brain_system import BrainSystem

logger = logging.getLogger(__name__)


# ----- Agent Activity Tracker -----
_TRACKED_AGENTS: dict[str, str] = {}
_AGENT_LOGGERS: dict[str, logging.Logger] = {}


def setup_tracked_agents(agent_ids_and_names: list[tuple[str, str]]) -> list[str]:
    """Configure per-agent log files for tracked agents. Returns list of agent IDs."""
    global _TRACKED_AGENTS, _AGENT_LOGGERS

    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "logs", "agents",
    )
    os.makedirs(log_dir, exist_ok=True)

    _TRACKED_AGENTS.clear()
    _AGENT_LOGGERS.clear()

    for agent_id, name in agent_ids_and_names:
        _TRACKED_AGENTS[agent_id] = name

        log_file = os.path.join(log_dir, f"{name}.log")

        ag_logger = logging.getLogger(f"agentropolis.agent.{name}")
        ag_logger.setLevel(logging.DEBUG)
        for h in list(ag_logger.handlers):
            ag_logger.removeHandler(h)

        fh = logging.FileHandler(log_file, mode="w")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-5s | %(message)s",
            datefmt="%H:%M:%S",
        ))
        ag_logger.addHandler(fh)
        _AGENT_LOGGERS[agent_id] = ag_logger

        ag_logger.info(f"=== Tracking started for {name} (id={agent_id}) ===")

    logger.info(f"Tracking {len(_TRACKED_AGENTS)} agents: {', '.join(_TRACKED_AGENTS.values())}")
    return [aid for aid, _ in agent_ids_and_names]


def log_agent_activity(agent_id: str, action: str, detail: str, level: str = "INFO"):
    """Log activity for a tracked agent if they are being followed."""
    ag_logger = _AGENT_LOGGERS.get(agent_id)
    if ag_logger:
        name = _TRACKED_AGENTS[agent_id]
        method = getattr(ag_logger, level.lower(), ag_logger.info)
        method(f"[{name}] {action} - {detail}")


class AgentropolisSimulation:
    """Main simulation engine."""
    
    def __init__(self, tick_rate: float = 10.0, llm_agent_ids: list[str] | None = None):
        self.tick_rate = tick_rate
        self.tick_interval = 1.0 / tick_rate
        self.running = False
        self.brain_system = BrainSystem()
        self.tick_count = 0
        self._llm_agent_ids = set(llm_agent_ids or [])
        if self._llm_agent_ids:
            self.brain_system.register_llm_agents(self._llm_agent_ids)
            logger.info(f"LLM brains enabled for {len(self._llm_agent_ids)} tracked agents")
        
    async def initialize(self):
        """Initialize the simulation."""
        logger.info("Initializing Agentropolis simulation...")
        await self._load_world_state()
        logger.info("Simulation initialized")
    
    async def _load_world_state(self) -> tuple[List[Agent], List[Location]]:
        """Load agents and locations from database."""
        async with AsyncSessionLocal() as session:
            from sqlalchemy import select
            
            agents_result = await session.execute(
                select(Agent).where(Agent.is_active == True)
            )
            agents = list(agents_result.scalars().all())
            
            locations_result = await session.execute(select(Location))
            locations = list(locations_result.scalars().all())
            
            logger.info(f"Loaded {len(agents)} agents and {len(locations)} locations")
            return agents, locations
    
    async def _update_agent_states(
        self, agents: List[Agent], decisions: List[dict], locations: List[Location]
    ):
        """Update agent states based on their decisions."""
        async with AsyncSessionLocal() as session:
            from sqlalchemy import select, update
            
            agent_dict = {str(agent.id): agent for agent in agents}
            location_dict = {str(loc.id): loc for loc in locations}
            
            for decision in decisions:
                agent_id = UUID(decision["agent_id"])
                agent = agent_dict.get(decision["agent_id"])
                if not agent:
                    continue
                
                action_type = decision["action_type"]
                target_id = decision["target_id"]
                params = decision["parameters"]
                
                if action_type == "move":
                    await self._handle_move(agent, target_id, params, session, location_dict)
                elif action_type == "work":
                    await self._handle_work(agent, target_id, params, session)
                elif action_type == "socialize":
                    await self._handle_socialize(agent, target_id, params, session, agent_dict)
                elif action_type == "idle":
                    await self._handle_idle(agent, params, session)
                
            await session.commit()
    
    async def _handle_move(
        self, agent: Agent, target_id: Optional[str], params: dict,
        session, location_dict: dict
    ):
        """Handle movement action."""
        if target_id and target_id in location_dict:
            target_location = location_dict[target_id]
            old_location_id = agent.location_id
            agent.location_id = target_location.id
            agent.x = target_location.x
            agent.y = target_location.y
            
            if old_location_id:
                pass  # Separate cleanup pass
            target_location.current_occupancy += 1
                
            distance = 1.0
            agent.energy = max(0, agent.energy - int(distance * 5))
            
            logger.debug(f"{agent.name} moved to {target_location.name}")
            log_agent_activity(
                str(agent.id), "move",
                f"{agent.name} moved to {target_location.name} (energy: {agent.energy})",
            )
        elif params.get("wander"):
            agent.x += random.uniform(-1, 1)
            agent.y += random.uniform(-1, 1)
            agent.energy = max(0, agent.energy - 2)
            logger.debug(f"{agent.name} wandered")
            log_agent_activity(
                str(agent.id), "wander",
                f"{agent.name} wandered to ({agent.x:.1f}, {agent.y:.1f}) (energy: {agent.energy})",
            )

    async def _handle_work(
        self, agent: Agent, target_id: Optional[str], params: dict, session
    ):
        """Handle work action."""
        if target_id:
            duration = params.get("duration", 1)
            money_earned = duration * 10
            energy_cost = duration * 5
            hunger_increase = duration * 3
            
            agent.money += money_earned
            agent.energy = max(0, agent.energy - energy_cost)
            agent.hunger = min(100, agent.hunger + hunger_increase)
            
            logger.debug(f"{agent.name} worked and earned {money_earned} money")
            log_agent_activity(
                str(agent.id), "work",
                f"{agent.name} earned {money_earned:.1f} money (energy: {agent.energy}, hunger: {agent.hunger})",
            )
    
    async def _handle_socialize(
        self, agent: Agent, target_id: Optional[str], params: dict,
        session, agent_dict: dict
    ):
        """Handle socialize action."""
        if target_id and target_id in agent_dict:
            target_agent = agent_dict[target_id]
            happiness_gain = 5
            agent.happiness = min(100, agent.happiness + happiness_gain)
            target_agent.happiness = min(100, target_agent.happiness + happiness_gain)
            
            agent.energy = max(0, agent.energy - 2)
            
            logger.debug(f"{agent.name} socialized with {target_agent.name}")
            log_agent_activity(
                str(agent.id), "socialize",
                f"{agent.name} socialized with {target_agent.name} (happiness: {agent.happiness})",
            )
    
    async def _handle_idle(self, agent: Agent, params: dict, session):
        """Handle idle action."""
        duration = params.get("duration", 1)
        agent.energy = min(100, agent.energy + duration)
        agent.hunger = min(100, agent.hunger + duration // 2)
        
        logger.debug(f"{agent.name} idled for {duration} ticks")
        log_agent_activity(
            str(agent.id), "idle",
            f"{agent.name} idled (energy: {agent.energy}, hunger: {agent.hunger})",
        )
    
    async def _apply_needs_decay(self, agents: List[Agent]):
        """Apply natural decay to agent needs over time."""
        for agent in agents:
            agent.hunger = min(100, agent.hunger + 1)
            agent.energy = max(0, agent.energy - 1)
            
            if agent.happiness > 0:
                agent.happiness = max(0, agent.happiness - 1)
            elif agent.happiness < 0:
                agent.happiness = min(0, agent.happiness + 1)
                
            if agent.hunger > 90:
                agent.health = max(0, agent.health - 2)
            elif agent.hunger > 70:
                agent.health = max(0, agent.health - 1)
    
    async def tick(self):
        """Execute one simulation tick."""
        self.tick_count += 1
        logger.debug(f"--- Tick {self.tick_count} ---")
        
        agents, locations = await self._load_world_state()
        
        if not agents:
            logger.warning("No active agents in simulation")
            return
        
        decisions = await self.brain_system.process_agents(agents, locations)
        
        await self._update_agent_states(agents, decisions, locations)
        
        await self._apply_needs_decay(agents)
        
        # Log tracked agent status every tick
        for agent in agents:
            aid = str(agent.id)
            if aid in _AGENT_LOGGERS:
                log_agent_activity(
                    aid, "tick",
                    f"Tick {self.tick_count} | energy={agent.energy} hunger={agent.hunger} happiness={agent.happiness} health={agent.health} money={agent.money:.1f}",
                )
        
        if self.tick_count % 50 == 0:
            avg_happiness = sum(a.happiness for a in agents) / len(agents)
            avg_energy = sum(a.energy for a in agents) / len(agents)
            avg_hunger = sum(a.hunger for a in agents) / len(agents)
            logger.info(
                f"Tick {self.tick_count}: "
                f"Pop={len(agents)}, "
                f"Avg Happiness={avg_happiness:.1f}, "
                f"Avg Energy={avg_energy:.1f}, "
                f"Avg Hunger={avg_hunger:.1f}"
            )
    
    async def run(self):
        """Run the main simulation loop."""
        await self.initialize()
        self.running = True
        logger.info(f"Starting simulation at {self.tick_rate} ticks/sec")
        
        while self.running:
            start_time = asyncio.get_event_loop().time()
            
            try:
                await self.tick()
            except Exception as e:
                logger.error(f"Error in simulation tick: {e}", exc_info=True)
            
            elapsed = asyncio.get_event_loop().time() - start_time
            sleep_time = max(0, self.tick_interval - elapsed)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
    
    def stop(self):
        """Stop the simulation."""
        self.running = False
        logger.info("Stopping simulation...")
        # Final dump of tracked agent states
        for name, ag_logger in _AGENT_LOGGERS.items():
            ag_logger.info("=== Tracking stopped ===")


# For running as a standalone script
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    sim = AgentropolisSimulation(tick_rate=10.0)
    
    try:
        asyncio.run(sim.run())
    except KeyboardInterrupt:
        logger.info("Simulation interrupted by user")
        sim.stop()
