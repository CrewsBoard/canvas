import asyncio
from typing import List, Optional, Dict, Any

from crewai import Task, Crew
from crewai.utilities.events import (
    CrewKickoffStartedEvent,
    CrewKickoffCompletedEvent,
    AgentExecutionCompletedEvent,
)
from crewai.utilities.events.base_event_listener import BaseEventListener

from flow_engine.flow_chain.dtos import NodeTypes, FlowNodeConfigs
from flow_engine.flow_chain.services import FlowNodeRegistry
from flow_engine.flow_chain.services.flow_node import FlowNode
from flow_engine.flow_node.crewai_agent_node.dtos.crewai_agent_node_dto import (
    CrewAIAgentNodeDTO,
    CrewAiAgentNodeConfiguration,
)


@FlowNodeRegistry.register("crewai_crew")
class CrewAiCrewNode(FlowNode, BaseEventListener):
    def __init__(self, config: FlowNodeConfigs):
        super().__init__(config)
        self.temp_removed_connections = []

    async def _initialize_crew(self) -> None:
        flow_chain_data = await self.flow_engine_service.read_flow_chains(
            self.flow_chain_id
        )
        self.flow_chain = flow_chain_data[0]
        self.agents = [
            agent_flow.agent
            for agent_flow in self.flow_engine_service.flow_engine_agent_factory.get(
                self.flow_chain_id
            )
        ]
        tasks = await self._create_tasks_from_chain()
        self.crew = Crew(
            agents=self.agents,
            tasks=tasks,
            verbose=True,
        )

    async def _create_tasks_from_chain(self) -> List[Task]:
        tasks = []

        for node in self.flow_chain.nodes:
            if isinstance(node, CrewAIAgentNodeDTO):
                node.configuration = CrewAiAgentNodeConfiguration.model_validate(
                    node.configuration
                )
                agent = next(
                    (
                        agent
                        for agent in self.agents
                        if agent.role == node.configuration.role
                    ),
                    None,
                )
                if agent:
                    task = Task(
                        description=f"Process the input data and perform your role as {agent.role}",
                        agent=agent,
                        expected_output=f"Output from {agent.role} based on the input data",
                    )
                    tasks.append(task)

        for connection in self.flow_chain.connections:
            source_node = next(
                (
                    node
                    for node in self.flow_chain.nodes
                    if node.id == connection.from_node_id
                ),
                None,
            )
            target_node = next(
                (
                    node
                    for node in self.flow_chain.nodes
                    if node.id == connection.to_node_id
                ),
                None,
            )

            if isinstance(source_node, CrewAIAgentNodeDTO) and isinstance(
                target_node, CrewAIAgentNodeDTO
            ):
                source_agent = next(
                    (
                        agent
                        for agent in self.agents
                        if agent.role == source_node.configuration.role
                    ),
                    None,
                )
                target_agent = next(
                    (
                        agent
                        for agent in self.agents
                        if agent.role == target_node.configuration.role
                    ),
                    None,
                )

                if source_agent and target_agent:
                    if connection.condition:
                        task = Task(
                            description=f"Only delegate to the poet if the {source_agent.role} response contains the exact string {connection.condition}. Otherwise, respond with a message explaining that poems can only be written about roses, apples, or doctors.",
                            agent=target_agent,
                            expected_output=f"Condition met for {target_agent.role}",
                        )
                        tasks.append(task)

        return tasks

    async def process(self, message: Optional[Dict[str, Any]] = None) -> None:
        await self._initialize_crew()
        await self.crew.kickoff_async(inputs=message)

    def get_crew(self) -> Crew:
        return self.crew

    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_started(source, event):
            print(f"Crew '{event.crew_name}' has started execution!")

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_completed(source, event):
            print(f"Crew '{event.crew_name}' has completed execution!")
            print(f"Output: {event.output}")
            for conn in self.temp_removed_connections:
                self.connections.append(conn)
            # @todo decide what to do with the output
            # asyncio.run(self.next({"message": event.output}))

        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_execution_completed(source, event):
            print(f"Agent '{event.agent.role}' completed task")
            print(f"Output: {event.output}")
            connected_agent = next(
                (
                    conn
                    for conn in self.connections
                    if conn.from_node_id == event.agent.role
                    and conn.to_node_type == NodeTypes.AGENT
                ),
                None,
            )
            if connected_agent and event.output != connected_agent.condition:
                connection_to_be_removed = next(
                    (
                        conn
                        for conn in self.connections
                        if conn.from_node_id == connected_agent.to_node_id
                    ),
                    None,
                )
                self.connections = [
                    conn
                    for conn in self.connections
                    if conn.from_node_id != connection_to_be_removed.from_node_id
                    and conn.to_node_id != connection_to_be_removed.to_node_id
                ]
                self.temp_removed_connections.append(connection_to_be_removed)
            asyncio.run(self.next({"message": event.output}, event.agent.role))
