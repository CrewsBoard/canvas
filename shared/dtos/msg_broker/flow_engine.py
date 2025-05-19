import time
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field


class FlowEngineNodeProcessingData(BaseModel):
    message: str


class FlowEngineMsg(BaseModel):
    timestamp: float = Field(default_factory=lambda: time.time() * 1000)
    flow_chain_id: UUID4
    data: FlowEngineNodeProcessingData
    # @todo transform to UUID4
    node_id: str
    start_node_id: str
    previous_node_id: Optional[str] = None
    history: List["FlowEngineMsg"] = Field(default_factory=list)
