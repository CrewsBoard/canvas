from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from crewai.tools import BaseTool
from crewai_tools.tools.serper_dev_tool.serper_dev_tool import SerperDevTool

from flow_engine.flow_chain.dtos.flow_node_configs import FlowNodeConfigs
from flow_engine.flow_chain.dtos.node_types import NodeTypes
from flow_engine.flow_node.crewai_agent_node.tools.format_output_tool import (
    prepare_transform_node_input,
)
from shared.dtos.msg_broker.flow_engine import FlowEngineMsg, FlowEngineNodeProcessingData
from shared.services.context_manager.context_manager_service import ContextManager
from shared.utils.logger import logger


class FlowNode(ABC, ContextManager):
    def __init__(self, config: FlowNodeConfigs):
        super().__init__()
        # @todo remove unnecessary params
        self.flow_chain_id = config.flow_chain_id
        self.id = config.node_id
        self.name = config.name
        self.type = config.node_type
        self.configuration = config.configuration or {}
        self.connections = config.connections or []
        self.current_message: Optional[FlowEngineMsg] = None

    async def __call__(self, message: Optional[FlowEngineMsg] = None) -> None:
        msg = None
        self.current_message = message
        if message:
            msg = message.data.model_dump()
        return await self.process(msg)

    @abstractmethod
    async def process(self, message: Optional[Dict[str, Any]] = None) -> None:
        """
        Process the incoming message and return the result.
        This method must be implemented by all flow nodes.
        """
        pass

    async def next(self, message: Dict[str, Any], node_id: Optional[str] = None) -> None:
        """
        Find out the next connected node and append the node into event queue for processing.
        """
        try:
            message = FlowEngineNodeProcessingData.model_validate(message)
        except Exception as e:
            raise Exception(f"Error validating message: {e}") from e

        next_msg = self.current_message.model_copy()
        node_id = node_id or self.id
        next_connection = next(
            (
                conn
                for conn in self.connections
                if conn.from_node_id == node_id
                if not (conn.from_node_type == NodeTypes.AGENT and conn.to_node_type == NodeTypes.AGENT)
            ),
            None,
        )
        if next_connection:
            if (
                next_connection.to_node_type == NodeTypes.AGENT and next_connection.from_node_type == NodeTypes.AGENT
            ) or (next_connection.from_node_type == NodeTypes.TOOL and next_connection.to_node_type == NodeTypes.AGENT):
                logger.warning(
                    f"{next_connection.from_node_type}({next_connection.from_node_id}) -> {next_connection.to_node_type}({next_connection.to_node_id}) connection is not supported"
                )
                return

            next_msg = FlowEngineMsg(
                flow_chain_id=self.flow_chain_id,
                node_id=next_connection.to_node_id,
                start_node_id=self.current_message.start_node_id,
                previous_node_id=self.id,
                data=message,
            )
            next_msg.history = self.current_message.history.copy()
            next_msg.history.append(FlowEngineMsg.model_validate(self.current_message.model_dump(exclude={"history"})))

            try:
                await self.flow_engine_service.next(self.flow_chain_id, next_msg)
            except Exception as e:
                raise Exception(f"Error publishing message: {e}") from e

            logger.info("Next message has been published for the execution")
            logger.info(f"{next_msg}")
        else:
            traversed_node_directions = [history.node_id for history in next_msg.history]
            traversed_node_directions.append(next_msg.node_id)
            logger.info("No next node found for the message.")
            logger.info(f"Traversed nodes: {'-> '.join(traversed_node_directions)}")

    def validate_configuration(self) -> bool:
        """
        Validate the node's configuration.
        Returns True if configuration is valid, False otherwise.
        """
        return True

    def get_metadata(self) -> Dict[str, Any]:
        """
        Return metadata about the node.
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "configuration": self.configuration,
        }

    # @todo make a tool discovery service
    @staticmethod
    def get_tools(tools: List[str]) -> List[BaseTool]:
        """Fetches tools based on the provided list of tool names."""
        # This function should be implemented to return the actual tools
        # For now, we will return an empty list
        parsed_tools: List[BaseTool] = []
        for tool in tools:
            if tool == "format_output_tool":
                parsed_tools.append(prepare_transform_node_input)
            elif tool == "SerperDevTool":
                parsed_tools.append(SerperDevTool())

        return parsed_tools
