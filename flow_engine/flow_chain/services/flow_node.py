from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List

from crewai.tools import BaseTool
from crewai_tools.tools.serper_dev_tool.serper_dev_tool import SerperDevTool, logger

from flow_engine.flow_chain.dtos import NodeConnection, NodeTypes
from flow_engine.flow_node.crewai_agent_node.tools.format_output_tool import (
    prepare_transform_node_input,
)
from shared.services.context_manager.context_manager_service import ContextManager


class FlowNode(ABC, ContextManager):
    def __init__(
        self,
        flow_chain_id: str,
        name: str,
        node_type: NodeTypes,
        node_id: Optional[str] = "flow_node",
        configuration: Optional[Dict[str, Any]] = None,
        connections: Optional[List[NodeConnection]] = None,
    ):
        super().__init__()
        self.flow_chain_id = flow_chain_id
        self.id = node_id
        self.name = name
        self.type = node_type
        self.configuration = configuration or {}
        self.connections = connections or []

    @abstractmethod
    def process(self, message: Dict[str, Any]) -> None:
        """
        Process the incoming message and return the result.
        This method must be implemented by all flow nodes.
        """
        pass

    def next(self, message: Dict[str, Any], node_id: Optional[str] = None) -> None:
        """
        Find out the next connected node and append the node into event queue for processing.
        """
        node_id = node_id or self.id
        next_connection = next(
            (
                conn
                for conn in self.connections
                if conn.from_node_id == node_id
                if not (
                    conn.from_node_type == NodeTypes.AGENT
                    and conn.to_node_type == NodeTypes.AGENT
                )
            ),
            None,
        )
        if "message" not in self.flow_chain_events[self.flow_chain_id].keys():
            self.flow_chain_events[self.flow_chain_id]["message"] = {}
        if next_connection:
            if (
                next_connection.to_node_type == NodeTypes.AGENT
                and next_connection.from_node_type == NodeTypes.AGENT
            ) or (
                next_connection.from_node_type == NodeTypes.TOOL
                and next_connection.to_node_type == NodeTypes.AGENT
            ):
                logger.warning(
                    f"{next_connection.from_node_type}({next_connection.from_node_id}) -> {next_connection.to_node_type}({next_connection.to_node_id}) connection is not supported"
                )
                return
            if (
                next_connection.to_node_id
                not in self.flow_chain_events[self.flow_chain_id]["traversed_node"]
            ):
                self.flow_chain_events[self.flow_chain_id]["traversed_node"].append(
                    next_connection.to_node_id
                )
            self.flow_chain_events[self.flow_chain_id]["message"][
                next_connection.to_node_id
            ] = message
            self.event.set()
        else:
            logger.warning(
                f"{', '.join(self.flow_chain_events[self.flow_chain_id]['traversed_node'])} completed"
            )
            logger.info(f"Final message: {self.flow_chain_events[self.flow_chain_id]}")

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
