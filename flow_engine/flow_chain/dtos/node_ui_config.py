from typing import List, Optional

from pydantic import BaseModel, UUID4

from .input_types import InputTypes
from .node_types import NodeTypes
from .output_types import OutputTypes


class NodeUiFields(BaseModel):
    label: str
    description: str
    type: Optional[str] = None
    default: Optional[object] = None
    required: Optional[bool] = None


class NodeUiConfig(BaseModel):
    id: Optional[UUID4] = None
    is_start_node: Optional[bool] = False
    debug_mode: Optional[bool] = False
    type: NodeTypes
    name: str
    title: str
    description: str
    icon: str
    color: str
    inputs: List[InputTypes]
    outputs: List[OutputTypes]
    fields: List[NodeUiFields]
