from pydantic import BaseModel, UUID4

from shared.dtos.msg_broker import FlowEngineNodeProcessingData


class FlowEngineExecuteParams(BaseModel):
    flow_chain_id: UUID4
    # @todo transform to UUID4
    start_node_id: str
    data: FlowEngineNodeProcessingData
