from datetime import datetime
from typing import Optional

from pydantic import UUID4
from sqlalchemy import DateTime, func, Column
from sqlmodel import Field

from core.repositories.schemas.base_schema import BaseSchema


class AgentSchema(BaseSchema, table=True):
    __tablename__ = "agents"

    name: str = Field(nullable=False)
    llm_id: Optional[UUID4] = Field(nullable=True)
    function_calling_llm_id: Optional[UUID4] = Field(nullable=True)
    max_iter: Optional[int] = Field(nullable=True)
    max_rpm: Optional[int] = Field(nullable=True)
    verbose: bool = Field(nullable=True)
    allow_delegation: bool = Field(nullable=True)
    embedder_id: Optional[UUID4] = Field(nullable=True)
    use_system_prompt: bool = Field(nullable=True)
    allow_code_execution: bool = Field(nullable=True)
    respect_context_window: bool = Field(nullable=True)
    max_retry_limit: Optional[int] = Field(nullable=True)
    multimodal: bool = Field(nullable=True)
    code_execution_mode: str = Field(nullable=True)
    max_execution_time: Optional[int] = Field(nullable=True)

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
    )
