from pydantic import UUID4
from sqlalchemy import PrimaryKeyConstraint
from sqlmodel import Field, SQLModel

from core.dtos.entity import EntityType


class RelationSchema(SQLModel, table=True):
    __tablename__ = 'relations'

    from_entity_id: UUID4 = Field(nullable=False)
    to_entity_id: UUID4 = Field(nullable=False)
    from_entity_type: EntityType = Field(nullable=False)
    to_entity_type: EntityType = Field(nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('from_entity_id', 'from_entity_type', 'to_entity_id', 'to_entity_type'),
    )
