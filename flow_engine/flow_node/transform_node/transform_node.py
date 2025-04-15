from typing import Dict, Any, List

from flow_engine.flow_chain.dtos import NodeTypes, NodeConnection
from flow_engine.flow_chain.services import FlowNodeRegistry
from flow_engine.flow_chain.services.flow_node import FlowNode


@FlowNodeRegistry.register("transform")
class TransformNode(FlowNode):
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
        Apply transformations to the message based on configuration.
        """
        result = message.copy()
        transformations = self.configuration.get("transformations", {})

        for field, transform_type in transformations.items():
            if field in result:
                if transform_type == "uppercase":
                    result[field] = str(result[field]).upper()
                elif transform_type == "increment":
                    if isinstance(result[field], (int, float)):
                        result[field] += 1
                elif transform_type == "reverse":
                    if isinstance(result[field], str):
                        result[field] = result[field][::-1]

        self.next(result)
