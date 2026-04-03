#!/usr/bin/env python3
"""
Entry point for running the Agentropolis simulation with ECS architecture.
"""
import asyncio
import logging
import signal
import sys
import time
from agentropolis.engine.world import AgentropolisWorld
from agentropolis.engine.systems import (
    MovementSystem,
    EcsBrainSystem,
    NeedsSystem,
    SocialSystem,
    EconomySystem
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('ecs_simulation.log')
    ]
)

logger = logging.getLogger(__name__)

# Global simulation instance for signal handling
simulation_world = None
simulation_running = False

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"Received signal {signum}, shutting down simulation...")
    global simulation_running
    simulation_running = False
    if simulation_world:
        # Final sync to database
        asyncio.create_task(simulation_world.sync_to_database())
    sys.exit(0)

async def main():
    """Main entry point for ECS-based simulation."""
    global simulation_world, simulation_running
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create ECS world
    simulation_world = AgentropolisWorld()
    
    try:
        logger.info("Initializing Agentropolis ECS simulation...")
        
        # Load initial state from database
        await simulation_world.initialize_from_database()
        
        # Get the ECS world and add systems
        ecs_world = simulation_world.get_world()
        
        # Add systems in order of dependency
        ecs_world.add_system(MovementSystem(ecs_world))
        ecs_world.add_system(EcsBrainSystem(ecs_world))
        ecs_world.add_system(NeedsSystem(ecs_world))
        ecs_world.add_system(SocialSystem(ecs_world))
        ecs_world.add_system(EconomySystem(ecs_world))
        
        logger.info(f"Added {len(ecs_world.systems)} systems to ECS world")
        
        # Start simulation loop
        simulation_running = True
        target_tick_rate = 10.0  # ticks per second
        tick_interval = 1.0 / target_tick_rate
        last_sync = time.time()
        sync_interval = 5.0  # seconds between database syncs
        
        logger.info(f"Starting ECS simulation at {target_tick_rate} ticks/sec")
        tick_count = 0
        
        while simulation_running:
            start_time = time.time()
            
            try:
                # Update ECS world (processes all systems)
                await ecs_world.update(tick_interval)
                tick_count += 1
                
                # Periodic logging
                if tick_count % 100 == 0:  # Every 10 seconds at 10 ticks/sec
                    agent_count = len([e for e in ecs_world.entities.values() 
                                     if e.has_component(lambda c: hasattr(c, '__class__') and c.__class__.__name__ == 'IdentityComponent')])
                    logger.info(f"Tick {tick_count}: {agent_count} agents active")
                
                # Periodic database sync
                current_time = time.time()
                if current_time - last_sync >= sync_interval:
                    await simulation_world.sync_to_database()
                    last_sync = current_time
                    logger.debug("Synced ECS world to database")
                
            except Exception as e:
                logger.error(f"Error in simulation tick: {e}", exc_info=True)
            
            # Maintain tick rate
            elapsed = time.time() - start_time
            sleep_time = max(0, tick_interval - elapsed)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        # Final sync before shutdown
        logger.info("Performing final database sync...")
        await simulation_world.sync_to_database()
        
    except Exception as e:
        logger.error(f"Simulation failed: {e}", exc_info=True)
        return 1
    finally:
        logger.info("ECS simulation has stopped.")
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)