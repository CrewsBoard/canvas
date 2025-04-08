from pydantic import BaseModel, UUID4

from core.dtos.entity import EntityType


class RelationDto(BaseModel):
    from_entity_id: UUID4
    to_entity_id: UUID4
    from_entity_type: EntityType
    to_entity_type: EntityType
