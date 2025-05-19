from typing import List

from pydantic import UUID4, BaseModel

from flow_engine.flow_chain.dtos.node_connection import NodeConnection
from flow_engine.flow_node.crewai_agent_node.dtos.crewai_agent_node_dto import CrewAIAgentNodeDTO, ToolNodeDto


class FlowChain(BaseModel):
    id: UUID4
    name: str
    description: str
    nodes: List[ToolNodeDto | CrewAIAgentNodeDTO]
    connections: List[NodeConnection]
    first_node_id: str
    debug_mode: bool = False
