"""Entity-Component-System core implementation."""
import uuid
from abc import ABC, abstractmethod
from typing import Dict, List, Type, Set, Optional, Any
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)

@dataclass
class Component:
    """Base class for all components."""
    entity_id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class Entity:
    """An entity in the ECS - just a collection of components."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    components: Dict[Type[Component], Component] = field(default_factory=dict)
    
    def add_component(self, component: Component):
        """Add a component to this entity."""
        component.entity_id = self.id
        self.components[type(component)] = component
        logger.debug(f"Added {type(component).__name__} to entity {self.id}")
    
    def get_component(self, component_type: Type[Component]) -> Optional[Component]:
        """Get a component of the specified type."""
        return self.components.get(component_type)
    
    def has_component(self, component_type: Type[Component]) -> bool:
        """Check if entity has a component of the specified type."""
        return component_type in self.components
    
    def remove_component(self, component_type: Type[Component]):
        """Remove a component from this entity."""
        if component_type in self.components:
            del self.components[component_type]
            logger.debug(f"Removed {component_type.__name__} from entity {self.id}")

class System(ABC):
    """Base class for all systems that process entities with specific components."""
    
    def __init__(self, world: 'World'):
        self.world = world
        self.required_components: Set[Type[Component]] = set()
        self.entity_cache: Set[uuid.UUID] = set()
        logger.debug(f"Initialized {self.__class__.__name__}")
    
    def add_entity(self, entity_id: uuid.UUID):
        """Add an entity to this system's processing list."""
        self.entity_cache.add(entity_id)
        logger.debug(f"System {self.__class__.__name__} now tracking entity {entity_id}")
    
    def remove_entity(self, entity_id: uuid.UUID):
        """Remove an entity from this system's processing list."""
        self.entity_cache.discard(entity_id)
        logger.debug(f"System {self.__class__.__name__} no longer tracking entity {entity_id}")
    
    @abstractmethod
    async def process(self, entities: Dict[uuid.UUID, 'Entity'], delta_time: float):
        """Process all tracked entities."""
        pass

@dataclass
class World:
    """The game world that holds entities and systems."""
    entities: Dict[uuid.UUID, Entity] = field(default_factory=dict)
    systems: List[System] = field(default_factory=list)
    _next_entity_id: int = 0
    
    def create_entity(self) -> Entity:
        """Create a new entity and add it to the world."""
        entity = Entity()
        self.entities[entity.id] = entity
        logger.debug(f"Created entity {entity.id}")
        return entity
    
    def destroy_entity(self, entity_id: uuid.UUID):
        """Remove an entity from the world."""
        if entity_id in self.entities:
            # Notify all systems
            for system in self.systems:
                system.remove_entity(entity_id)
            del self.entities[entity_id]
            logger.debug(f"Destroyed entity {entity_id}")
    
    def add_system(self, system: System):
        """Add a system to the world."""
        self.systems.append(system)
        logger.debug(f"Added system {system.__class__.__name__}")
        
        # Notify the system about existing entities
        for entity_id, entity in self.entities.items():
            if self._entity_matches_system(entity, system):
                system.add_entity(entity_id)
    
    def _entity_matches_system(self, entity: Entity, system: System) -> bool:
        """Check if an entity has all required components for a system."""
        for component_type in system.required_components:
            if not entity.has_component(component_type):
                return False
        return True
    
    async def update(self, delta_time: float):
        """Update all systems."""
        # Update entity cache for each system
        for system in self.systems:
            # Re-check which entities match this system
            system.entity_cache.clear()
            for entity_id, entity in self.entities.items():
                if self._entity_matches_system(entity, system):
                    system.add_entity(entity_id)
        
        # Process all systems
        for system in self.systems:
            try:
                await system.process(self.entities, delta_time)
            except Exception as e:
                logger.error(f"Error in system {system.__class__.__name__}: {e}", exc_info=True)
    
    def get_entities_with_components(self, *component_types: Type[Component]) -> List[Entity]:
        """Get all entities that have all specified components."""
        result = []
        for entity in self.entities.values():
            if all(entity.has_component(ct) for ct in component_types):
                result.append(entity)
        return result