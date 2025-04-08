from typing import Optional

from core.dtos.base import BaseDto
from core.dtos.task.task_priorities import TaskPriorities


class TaskDto(BaseDto):
    name: str
    context: Optional[str] = None
    async_execution: Optional[bool] = False
    human_input: Optional[bool] = False
    priority: Optional[TaskPriorities] = None
