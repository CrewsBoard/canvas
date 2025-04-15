import asyncio
from typing import Optional, Dict, Any, List

from crewai import Agent, LLM

from core.dtos.entity.model_entity import ModelEntity
from flow_engine.flow_chain.dtos import NodeConnection, NodeTypes
from flow_engine.flow_chain.services import FlowNodeRegistry
from flow_engine.flow_chain.services.agent_flow import AgentFlow
from flow_engine.flow_chain.services.flow_node import FlowNode
from flow_engine.flow_node.crewai_agent_node.dtos.crewai_agent_node_dto import (
    CrewAIAgentNodeDTO,
    CrewAiAgentNodeConfiguration,
)


@FlowNodeRegistry.register("crewai_agent")
class CrewAiAgentNode(FlowNode):
    def __init__(
        self,
        flow_chain_id: str,
        node_id: str,
        name: str,
        node_type: NodeTypes,
        configuration: Dict[str, Any] = None,
        connections: List[NodeConnection] = None,
    ):
        super().__init__(
            flow_chain_id=flow_chain_id,
            node_id=node_id,
            name=name,
            node_type=node_type,
            configuration=configuration,
            connections=connections,
        )
        self.node_data = CrewAIAgentNodeDTO(
            id=node_id,
            name=name,
            node_type=node_type,
            configuration=CrewAiAgentNodeConfiguration.model_validate(configuration),
            node_template_id="crewai_agent",
        )
        self.connections = connections
        self.agent: Optional[Agent] = None
        self.connected_nodes: List[Dict[str, Any]] = []
        # Create a task for async initialization
        asyncio.create_task(self._initialize_agent())

    async def _initialize_agent(self) -> None:
        for conn in self.connections:
            if conn.from_node_id == self.node_data.id:
                has_connection_to_agent_node = conn.to_node_type == NodeTypes.AGENT
                if has_connection_to_agent_node:
                    self.node_data.allow_delegation = True
                    if conn.condition:
                        self.node_data.configuration.goal += f"{conn.condition}"
                        self.node_data.configuration.backstory += f" {conn.condition}"

        self.agent = Agent(
            agent_ops_agent_name="crewai_agent",
            role=self.node_data.configuration.role,
            goal=self.node_data.configuration.goal,
            backstory=self.node_data.configuration.backstory,
            tools=self.get_tools(self.node_data.configuration.tools),
            verbose=True,
            llm=await self.get_model(),
            max_iter=self.node_data.configuration.max_iterations or 25,
        )
        output_event = asyncio.Event()
        if not self.agent_service.agent_flows:
            self.agent_service.agent_flows[self.flow_chain_id] = []
        self.agent_service.agent_flows[self.flow_chain_id].append(
            AgentFlow(
                agent=self.agent,
                flow_chain_id=self.flow_chain_id,
                output_event=output_event,
            )
        )

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def get_agent(self) -> Optional[Agent]:
        return self.agent

    async def update_agent(
        self,
        node_data: Optional[CrewAIAgentNodeDTO] = None,
        connections: Optional[List[NodeConnection]] = None,
    ) -> None:
        has_updated = False
        if node_data:
            self.node_data = node_data
            has_updated = True
        if connections:
            self.connections = connections
            has_updated = True
        if has_updated:
            await self._initialize_agent()

    # @todo make this properly asinc in fun level
    async def get_model(self) -> LLM:
        return await self.model_service.build(
            ModelEntity(self.node_data.configuration.model_id)
        )
