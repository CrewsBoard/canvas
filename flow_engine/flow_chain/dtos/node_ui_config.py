from typing import List, Optional

from pydantic import UUID4, BaseModel

from flow_engine.flow_chain.dtos.input_types import InputTypes
from flow_engine.flow_chain.dtos.node_types import NodeTypes
from flow_engine.flow_chain.dtos.output_types import OutputTypes


class NodeUiFields(BaseModel):
    label: str
    description: str
    type: Optional[str] = None
    default: Optional[object] = None
    required: Optional[bool] = None


# @todo refactor or remove unnecessary fields
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
    node_template_id: str
    ui_bundle: Optional[str] = None
