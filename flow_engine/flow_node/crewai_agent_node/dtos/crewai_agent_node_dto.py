from typing import List, Optional

from crewai.tools import BaseTool
from pydantic import BaseModel, UUID4

from flow_engine.flow_chain.dtos.node_types import NodeTypes


class CrewAiAgentNodeConfiguration(BaseModel):
    role: str
    goal: str
    backstory: str
    tools: List[str] = ([],)
    max_iterations: Optional[int] = None
    allow_delegation: Optional[bool] = None
    model_id: Optional[UUID4] = None


class ToolNodeDto(BaseModel):
    id: str
    name: str
    node_type: NodeTypes
    configuration: dict


class CrewAIAgentNodeDTO(BaseModel):
    id: str
    name: str
    node_type: NodeTypes
    configuration: CrewAiAgentNodeConfiguration
    allow_delegation: Optional[bool] = False
    tools: Optional[List[BaseTool]] = []
