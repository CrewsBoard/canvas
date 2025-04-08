from datetime import datetime

from sqlalchemy import DateTime, func, Column
from sqlmodel import Field

from core.repositories.schemas.base_schema import BaseSchema


class TaskSchema(BaseSchema, table=True):
    __tablename__ = "tasks"

    name: str = Field(nullable=False)
    context: str = Field(nullable=True)
    async_execution: bool = Field(nullable=True)
    human_input: bool = Field(nullable=True)
    priority: str = Field(nullable=True)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
    )
