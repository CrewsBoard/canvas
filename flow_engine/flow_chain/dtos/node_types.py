from enum import Enum


class NodeTypes(str, Enum):
    AGENT = "agent"
    CONDITION = "condition"
    TOOL = "tool"
