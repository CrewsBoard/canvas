from dataclasses import dataclass
from typing import List, Any

from .node_connection import NodeConnection


@dataclass
class FlowChain:
    id: str
    name: str
    nodes: List[Any]
    connections: List[NodeConnection]
    first_node_id: str
    debug_mode: bool = False
