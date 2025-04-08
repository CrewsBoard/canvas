from typing import Optional

from pydantic import UUID4

from core.dtos.agent.code_execution_modes import CodeExecutionModes
from core.dtos.base import BaseDto


class AgentDto(BaseDto):
    name: str
    llm_id: Optional[UUID4] = None
    function_calling_llm_id: Optional[UUID4] = None
    max_iter: Optional[int] = None
    max_rpm: Optional[int] = None
    verbose: bool = False
    allow_delegation: bool = False
    embedder_id: Optional[UUID4] = None
    use_system_prompt: bool = False
    allow_code_execution: bool = False
    respect_context_window: bool = True
    max_retry_limit: Optional[int] = None
    multimodal: bool = False
    code_execution_mode: CodeExecutionModes = CodeExecutionModes.SAFE
    max_execution_time: Optional[int] = None
