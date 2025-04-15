from typing import List

from pydantic import BaseModel

from .node_connection import NodeConnection
from ...flow_node.crewai_agent_node.dtos.crewai_agent_node_dto import (
    ToolNodeDto,
    CrewAIAgentNodeDTO,
)


class FlowChain(BaseModel):
    id: str
    name: str
    description: str
    nodes: List[ToolNodeDto | CrewAIAgentNodeDTO]
    connections: List[NodeConnection]
    first_node_id: str
    debug_mode: bool = False
