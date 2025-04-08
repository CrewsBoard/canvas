from enum import Enum


class PromptTypes(str, Enum):
    ROLE = "role"
    GOAL = "goal"
    BACKSTORY = "backstory"
    SYSTEM_TEMPLATE = "system_template"
    PROMPT_TEMPLATE = "prompt_template"
    RESPONSE_TEMPLATE = "response_template"
    DESCRIPTION = "description"
    EXPECTED_OUTPUT = "expected_output"
    CONTEXT = "context"
