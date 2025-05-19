from pydantic import UUID4, BaseModel

from core.dtos.entity.entity_type import EntityType


class RelationDto(BaseModel):
    from_entity_id: UUID4
    to_entity_id: UUID4
    from_entity_type: EntityType
    to_entity_type: EntityType
