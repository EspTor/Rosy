#!/usr/bin/env python3
"""
Entry point for running the Agentropolis simulation.

On startup it picks 5 random active agents and writes individual
log files into agentropolis/logs/agents/<AgentName>.log
"""
import sys
import os

# Load .env BEFORE any other imports so API keys are available
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv(os.path.join(_PROJECT_ROOT, ".env"))

import asyncio
import logging
import signal

from agentropolis.simulation import AgentropolisSimulation, setup_tracked_agents
from agentropolis.database import async_engine

logger = logging.getLogger(__name__)

# Global simulation instance for signal handling
simulation = None


async def _pick_tracked_agents() -> list[tuple[str, str]]:
    """Return 5 random active agents as (id_str, name) from the DB."""
    from sqlalchemy import text

    async with async_engine.connect() as conn:
        rows = await conn.execute(text(
            "SELECT id::text, name FROM agents WHERE is_active = true "
            "ORDER BY RANDOM() LIMIT 5"
        ))
        return [(str(r[0]), r[1]) for r in rows]


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"Received signal {signum}, shutting down simulation...")
    if simulation:
        simulation.stop()
    sys.exit(0)


async def main():
    """Main entry point."""
    global simulation

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    tracked = await _pick_tracked_agents()
    llm_agent_ids: list[str] = []
    if tracked:
        agent_ids = setup_tracked_agents(tracked)
        llm_agent_ids = agent_ids  # all tracked agents get LLM brains
        print("\nTracking these agents (with LLM brains):")
        for aid, name in tracked:
            print(f"  {name}  ({aid})")
        print()
    else:
        logger.warning("No active agents found to track!")

    simulation = AgentropolisSimulation(tick_rate=10.0, llm_agent_ids=llm_agent_ids)
    print("=== Log files ===")
    project_root = os.path.join(_PROJECT_ROOT, "logs", "agents")
    for _, name in tracked:
        print(f"  {project_root}/{name}.log")
    print()

    try:
        logger.info("Starting Agentropolis simulation...")
        await simulation.run()
    except Exception as e:
        logger.error(f"Simulation failed: {e}", exc_info=True)
        return 1
    finally:
        logger.info("Simulation has stopped.")
        simulation.stop()

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
