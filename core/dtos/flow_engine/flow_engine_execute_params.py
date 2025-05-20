from pydantic import UUID4, BaseModel

from shared.dtos.msg_broker.flow_engine import FlowEngineNodeProcessingData


class FlowEngineExecuteParams(BaseModel):
    flow_chain_id: UUID4
    # @todo transform to UUID4
    start_node_id: str
    data: FlowEngineNodeProcessingData
