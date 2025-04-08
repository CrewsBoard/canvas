from core.repositories.base_repository import BaseRepository
from core.repositories.schemas.task_schema import TaskSchema
from core.services.database import database_service


class TaskRepository(BaseRepository[TaskSchema]):
    def __init__(self):
        super().__init__(database_service)
        self.schema = TaskSchema
