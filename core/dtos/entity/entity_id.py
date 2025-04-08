from pydantic import BaseModel, UUID4

from .entity_type import EntityType


class EntityId(BaseModel):
    id: UUID4
    type: EntityType
