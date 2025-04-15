from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func, Column
from sqlmodel import Field

from core.repositories.schemas.base_schema import BaseSchema


class ModelSchema(BaseSchema, table=True):
    __tablename__ = "models"

    name: str = Field(nullable=False)
    provider: str = Field(nullable=False)
    connection_url: str = Field(nullable=False)
    model_type: str = Field(nullable=False)
    description: Optional[str] = Field(nullable=True)
    api_key: Optional[str] = Field(nullable=True)
    # @todo add is_default prop

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
    )
