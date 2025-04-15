from typing import Dict, Any, List

from flow_engine.flow_chain.dtos import NodeTypes, NodeConnection
from flow_engine.flow_chain.services import FlowNodeRegistry
from flow_engine.flow_chain.services.flow_node import FlowNode


@FlowNodeRegistry.register("output")
class OutputNode(FlowNode):
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

    def process(self, message: Dict[str, Any]):
        """
        Process the output message based on configuration.
        """
        self.next(message)
