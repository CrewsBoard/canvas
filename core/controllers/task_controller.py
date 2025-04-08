from fastapi import APIRouter
from pydantic import UUID4

from core.controllers import BaseController
from core.dtos.task import TaskDto


class TaskController(BaseController):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(tags=self.task_swagger_tags)

        self.router.add_api_route("/tasks", self.read_all, methods=["GET"])
        self.router.add_api_route("/task/{task_id}", self.get, methods=["GET"])
        self.router.add_api_route("/task", self.create, methods=["POST"])
        self.router.add_api_route("/task/{task_id}", self.update, methods=["PUT"])
        self.router.add_api_route("/task/{task_id}", self.delete, methods=["DELETE"])

    async def read_all(self) -> list[TaskDto]:
        return await self.task_service.read_all()

    async def get(self, task_id: UUID4) -> TaskDto:
        return await self.task_service.read(task_id)

    async def create(self, task: TaskDto) -> TaskDto:
        return await self.task_service.create(task)

    async def update(self, task_id: UUID4, task: TaskDto) -> TaskDto:
        return await self.task_service.update(task_id, task)

    async def delete(self, task_id: UUID4) -> bool:
        return await self.task_service.delete(task_id)
