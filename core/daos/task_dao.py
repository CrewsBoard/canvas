from core.daos.base_dao import BaseDao
from core.dtos.task.task_dto import TaskDto
from core.repositories.schemas.task_schema import TaskSchema
from core.repositories.task_repository import TaskRepository


class TaskDao(BaseDao[TaskDto, TaskSchema]):
    def __init__(self, task_repository: TaskRepository) -> None:
        super().__init__(task_repository)
        self.dto = TaskDto
        self.schema = TaskSchema
