from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class NodeConnection:
    from_node_id: str
    to_node_id: str
    label: str


class FlowChain:
    def __init__(
        self,
        id: str,
        name: str,
        nodes: List[Any],
        connections: List[NodeConnection],
        first_node_id: str,
        debug_mode: bool = False,
    ):
        self.id = id
        self.name = name
        self.nodes = {node.id: node for node in nodes}
        self.connections = connections
        self.first_node_id = first_node_id
        self.debug_mode = debug_mode

    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a message through the flow chain.
        """
        current_node_id = self.first_node_id
        result = message

        while current_node_id:
            if self.debug_mode:
                print(f"Processing node: {current_node_id}")

            current_node = self.nodes[current_node_id]
            result = current_node.process(result)

            if self.debug_mode:
                print(f"Node {current_node_id} result: {result}")

            next_connection = next(
                (
                    conn
                    for conn in self.connections
                    if conn.from_node_id == current_node_id
                ),
                None,
            )

            if not next_connection:
                break

            current_node_id = next_connection.to_node_id

        return result

    def get_metadata(self) -> Dict[str, Any]:
        """
        Return metadata about the flow chain.
        """
        return {
            "id": self.id,
            "name": self.name,
            "nodes": [node.get_metadata() for node in self.nodes.values()],
            "connections": [
                {"from": conn.from_node_id, "to": conn.to_node_id, "label": conn.label}
                for conn in self.connections
            ],
            "first_node_id": self.first_node_id,
        }
