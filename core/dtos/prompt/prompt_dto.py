from core.dtos.base import BaseDto
from core.dtos.prompt.prompt_types import PromptTypes


class PromptDto(BaseDto):
    type: PromptTypes
    value: str
