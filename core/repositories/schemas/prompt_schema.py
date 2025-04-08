from datetime import datetime

from sqlalchemy import DateTime, func, Column
from sqlmodel import Field

from core.repositories.schemas.base_schema import BaseSchema


class PromptSchema(BaseSchema, table=True):
    __tablename__ = 'prompts'

    type: str = Field(nullable=False)
    value: str = Field(nullable=False)

    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))
