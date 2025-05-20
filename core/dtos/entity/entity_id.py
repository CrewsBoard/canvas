from pydantic import UUID4, BaseModel

from core.dtos.entity.entity_type import EntityType


class EntityId(BaseModel):
    id: UUID4
    type: EntityType
