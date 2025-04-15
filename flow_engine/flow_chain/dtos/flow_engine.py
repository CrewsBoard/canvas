from typing import Dict, Any, List, Optional

from pydantic import BaseModel

from .node_ui_config import NodeUiConfig


class NodeRequest(BaseModel):
    name: str
    type: str
    configuration: Dict[str, Any]
    debug_mode: bool = True
    singleton_mode: bool = False
    queue_name: Optional[str] = None
    additional_info: Dict[str, Any] = {}


class ConnectionRequest(BaseModel):
    from_node: str
    to_node: str
    type: str


class FlowChainRequest(BaseModel):
    name: str
    nodes: List[NodeRequest]
    connections: List[ConnectionRequest]
    first_node_id: str
    debug_mode: bool = False


class FlowEngineRequest(BaseModel):
    name: str
    nodes: List[NodeUiConfig]
    connections: List[ConnectionRequest]
    first_node_id: str
    debug_mode: bool = False


class MessageRequest(BaseModel):
    data: Dict[str, Any]


class FlowChainResponse(BaseModel):
    id: str
    name: str
    status: str
    message: str
