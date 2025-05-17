import asyncio
import json
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
)
from flow_engine.flow_node.crewai_crew_node.dtos.crewai_agent_response import (
    CrewaiAgentResponse,
)
from shared.utils.logger import logger


@FlowNodeRegistry.register("crewai_crew")
class CrewAiCrewNode(FlowNode, BaseEventListener):
    TASK_EXPECTED_OUTPUT = """Your final answer MUST be a JSON string formatted exactly as follows:
    {
      "output": "<Your full result or response from executing the task>",
      "is_valid": <true if you believe you successfully completed the {} task based on your instructions, false if you were unable to complete the task or ran into limitations, uncertainty, unable to produce the expected answer or missing information>
    }
    Ensure no other text precedes or follows this JSON object.
    """

    def __init__(self, config: FlowNodeConfigs):
        super().__init__(config)
        self.temp_removed_connections = []
        self.pending_messages = []
        self._process_task = None
        self._is_crew_finished = False
        self._condition_status_of_agent: Dict[str, bool] = {}

    async def _process_pending_messages(self):
        while True:
            if self.pending_messages:
                msg, role = self.pending_messages.pop(0)
                await self.next(msg, role)
            else:
                if self._is_crew_finished:
                    logger.info("Crew has finished processing all messages.")
                    self._process_task = None
                    self._condition_status_of_agent = {}
                    break
            await asyncio.sleep(0)

    async def _initialize_crew(self) -> None:
        self._is_crew_finished = False
        flow_chain_data = await self.flow_engine_service.read_flow_chains(
            self.flow_chain_id
        )
        self.flow_chain = flow_chain_data[0]
        self.agents = [
            agent
            for agent in self.flow_engine_service.flow_engine_agent_factory.get(
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
                    task = Task(
                        description=f"Perform the task of {source_agent.role} agent.",
                        agent=source_agent,
                        expected_output=f"{self.TASK_EXPECTED_OUTPUT.replace('{}', source_agent.role)}",
                    )
                    tasks.append(task)
                    if connection.condition:
                        task = Task(
                            description=f"Only perform the task of {target_agent.role} agent if the {source_agent.role} agent's response contains the exact string {connection.condition}. Otherwise, respond with a message explaining that can not delegate.",
                            agent=target_agent,
                            expected_output=f"{self.TASK_EXPECTED_OUTPUT.replace('{}', target_agent.role)}",
                        )
                        tasks.append(task)
                    else:
                        task = Task(
                            description=f"Perform the task of {target_agent.role} agent.",
                            agent=target_agent,
                            expected_output=f"{self.TASK_EXPECTED_OUTPUT.replace('{}', target_agent.role)}",
                        )
                        tasks.append(task)

        return tasks

    async def process(self, message: Optional[Dict[str, Any]] = None) -> None:
        if self._process_task is None or self._process_task.done():
            self._process_task = asyncio.create_task(self._process_pending_messages())

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
            self._is_crew_finished = True

        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_execution_completed(source, event):
            print(f"Agent '{event.agent.role}' completed task")
            print(f"Output: {event.output}")
            try:
                output_dict = json.loads(event.output)
                agent_output = CrewaiAgentResponse.model_validate(output_dict)
            except json.JSONDecodeError:
                raise Exception("Invalid JSON format in agent output")
            connected_agent = next(
                (
                    conn
                    for conn in self.connections
                    if conn.from_node_id == event.agent.role
                    and conn.to_node_type == NodeTypes.AGENT
                ),
                None,
            )
            if agent_output.is_valid:
                if connected_agent:
                    if connected_agent.from_node_id == event.agent.role:
                        if agent_output.output == connected_agent.condition:
                            self._condition_status_of_agent[
                                connected_agent.to_node_id
                            ] = True
                        self.pending_messages.append(
                            ({"message": agent_output.output}, event.agent.role)
                        )
                else:
                    if self._condition_status_of_agent.get(event.agent.role, False):
                        self.pending_messages.append(
                            ({"message": agent_output.output}, event.agent.role)
                        )
