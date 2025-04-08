from typing import ClassVar

from core.dtos.entity import EntityType
from core.dtos.entity.entity import Entity


class PromptEntity(Entity):
    entity_type: ClassVar[EntityType] = EntityType.PROMPT

    def __init__(self, entity_id: str):
        super().__init__(id=entity_id, type=self.entity_type)
