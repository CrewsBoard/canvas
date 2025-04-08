from fastapi import APIRouter
from pydantic import UUID4

from core.controllers.base_controller import BaseController
from core.dtos.model import ModelDto


class ModelController(BaseController):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(tags=self.model_swagger_tags)

        self.router.add_api_route("/models", self.read_all, methods=["GET"])
        self.router.add_api_route("/model/{model_id}", self.get, methods=["GET"])
        self.router.add_api_route("/model", self.create, methods=["POST"])
        self.router.add_api_route("/model/{model_id}", self.update, methods=["PUT"])
        self.router.add_api_route("/model/{model_id}", self.delete, methods=["DELETE"])

    async def read_all(self) -> list[ModelDto]:
        return await self.model_service.read_all()

    async def get(self, model_id: UUID4) -> ModelDto:
        return await self.model_service.read(model_id)

    async def create(self, model: ModelDto) -> ModelDto:
        return await self.model_service.create(model)

    async def update(self, model_id: UUID4, model: ModelDto) -> ModelDto:
        return await self.model_service.update(model_id, model)

    async def delete(self, model_id: UUID4) -> bool:
        return await self.model_service.delete(model_id)
