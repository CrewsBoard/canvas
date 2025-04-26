from typing import Optional, List, Dict, Any

from pydantic import BaseModel, UUID4

from .node_connection import NodeConnection
from .node_types import NodeTypes


class FlowNodeConfigs(BaseModel):
    flow_chain_id: UUID4
    name: str
    node_type: NodeTypes
    node_id: str
    configuration: Optional[Dict[str, Any]] = None
    connections: Optional[List[NodeConnection]] = None
