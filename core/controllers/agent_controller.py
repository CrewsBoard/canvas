from fastapi import APIRouter
from pydantic import UUID4

from core.controllers.base_controller import BaseController
from core.dtos.agent import AgentDto


class AgentController(BaseController):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(tags=self.agent_swagger_tags)

        self.router.add_api_route("/agents", self.read_all, methods=["GET"])
        self.router.add_api_route("/agent/{agent_id}", self.get, methods=["GET"])
        self.router.add_api_route("/agent", self.create, methods=["POST"])
        self.router.add_api_route("/agent/{agent_id}", self.update, methods=["PUT"])
        self.router.add_api_route("/agent/{agent_id}", self.delete, methods=["DELETE"])

    async def read_all(self) -> list[AgentDto]:
        return await self.agent_service.read_all()

    async def get(self, agent_id: UUID4) -> AgentDto:
        return await self.agent_service.read(agent_id)

    async def create(self, agent: AgentDto) -> AgentDto:
        return await self.agent_service.create(agent)

    async def update(self, agent_id: UUID4, agent: AgentDto) -> AgentDto:
        return await self.agent_service.update(agent_id, agent)

    async def delete(self, agent_id: UUID4) -> bool:
        return await self.agent_service.delete(agent_id)
