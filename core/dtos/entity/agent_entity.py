from typing import ClassVar

from core.dtos.entity import EntityType
from core.dtos.entity.entity import Entity


class AgentEntity(Entity):
    entity_type: ClassVar[EntityType] = EntityType.AGENT

    def __init__(self, entity_id: str):
        super().__init__(id=entity_id, type=self.entity_type)
