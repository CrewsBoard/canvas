from enum import Enum


class TaskPriorities(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
