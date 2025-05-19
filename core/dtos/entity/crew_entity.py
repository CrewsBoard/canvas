from typing import ClassVar

from core.dtos.entity.entity import Entity
from core.dtos.entity.entity_type import EntityType


class CrewEntity(Entity):
    entity_type: ClassVar[EntityType] = EntityType.CREW

    def __init__(self, entity_id: str) -> None:
        super().__init__(id=entity_id, type=self.entity_type)
