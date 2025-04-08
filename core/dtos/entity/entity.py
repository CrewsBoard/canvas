from pydantic import BaseModel, UUID4

from core.dtos.entity import EntityType


class Entity(BaseModel):
    id: UUID4
    type: EntityType
