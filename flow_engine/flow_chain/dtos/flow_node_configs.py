from typing import Any, Dict, List, Optional

from pydantic import UUID4, BaseModel

from flow_engine.flow_chain.dtos.node_connection import NodeConnection
from flow_engine.flow_chain.dtos.node_types import NodeTypes


class FlowNodeConfigs(BaseModel):
    flow_chain_id: UUID4
    name: str
    node_type: NodeTypes
    node_id: str
    configuration: Optional[Dict[str, Any]] = None
    connections: Optional[List[NodeConnection]] = None
