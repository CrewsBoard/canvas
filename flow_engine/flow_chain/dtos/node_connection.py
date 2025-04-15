from typing import Optional

from pydantic import BaseModel

from .node_types import NodeTypes


class NodeConnection(BaseModel):
    from_node_id: str
    to_node_id: str
    from_node_type: NodeTypes
    to_node_type: NodeTypes
    label: Optional[str] = None
    condition: Optional[str] = None
