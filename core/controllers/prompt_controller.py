from fastapi import APIRouter
from pydantic import UUID4

from core.controllers.base_controller import BaseController
from core.dtos.prompt import PromptDto


class PromptController(BaseController):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(tags=self.prompt_swagger_tags)

        self.router.add_api_route("/prompts", self.read_all, methods=["GET"])
        self.router.add_api_route("/prompt/{prompt_id}", self.get, methods=["GET"])
        self.router.add_api_route("/prompt", self.create, methods=["POST"])
        self.router.add_api_route("/prompt/{prompt_id}", self.update, methods=["PUT"])
        self.router.add_api_route("/prompt/{prompt_id}", self.delete, methods=["DELETE"])

    async def read_all(self) -> list[PromptDto]:
        return await self.prompt_service.read_all()

    async def get(self, prompt_id: UUID4) -> PromptDto:
        return await self.prompt_service.read(prompt_id)

    async def create(self, prompt: PromptDto) -> PromptDto:
        return await self.prompt_service.create(prompt)

    async def update(self, prompt_id: UUID4, prompt: PromptDto) -> PromptDto:
        return await self.prompt_service.update(prompt_id, prompt)

    async def delete(self, prompt_id: UUID4) -> bool:
        return await self.prompt_service.delete(prompt_id)
