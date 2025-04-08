from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field


class BaseSchema(SQLModel):
    id: Optional[UUID] = Field(
        default_factory=uuid4, primary_key=True, index=True, unique=True, nullable=False
    )
    created_by: Optional[UUID] = Field(nullable=False)
    updated_by: Optional[UUID] = Field(nullable=True)
