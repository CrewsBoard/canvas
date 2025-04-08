from datetime import datetime

from crewai import Process
from sqlalchemy import DateTime, func, Column
from sqlmodel import Field

from core.repositories.schemas.base_schema import BaseSchema


class CrewSchema(BaseSchema, table=True):
    __tablename__ = 'crews'

    name: str = Field(nullable=False)
    process: Process = Field(nullable=True, default=Process.sequential)
    verbose: bool = Field(nullable=True, default=False)

    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))
