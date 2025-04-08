from enum import Enum


class EntityType(str, Enum):
    PROMPT = "prompt"
    AGENT = "agent"
    TASK = "task"
    TOOL = "tool"
    CREW = "crew"
    MODEL = "model"
