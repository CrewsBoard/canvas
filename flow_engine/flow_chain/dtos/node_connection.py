from dataclasses import dataclass


@dataclass
class NodeConnection:
    from_node_id: str
    to_node_id: str
    label: str
