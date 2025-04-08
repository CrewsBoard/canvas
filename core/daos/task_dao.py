from core.daos.base_dao import BaseDao
from core.dtos.task import TaskDto
from core.repositories import TaskRepository
from core.repositories.schemas.task_schema import TaskSchema


class TaskDao(BaseDao[TaskDto, TaskSchema]):
    def __init__(self, task_repository: TaskRepository):
        super().__init__(task_repository)
        self.dto = TaskDto
        self.schema = TaskSchema
