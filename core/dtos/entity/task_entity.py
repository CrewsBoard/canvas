from typing import ClassVar

from core.dtos.entity.entity import Entity
from core.dtos.entity.entity_type import EntityType


class TaskEntity(Entity):
    entity_type: ClassVar[EntityType] = EntityType.TASK

    def __init__(self, entity_id: str) -> None:
        super().__init__(id=entity_id, type=self.entity_type)
