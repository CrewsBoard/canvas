from fastapi import APIRouter
from pydantic import UUID4

from core.controllers.base_controller import BaseController
from core.dtos.crew import CrewDto
from core.dtos.entity.crew_entity import CrewEntity


class CrewController(BaseController):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(tags=self.crew_swagger_tags)

        self.router.add_api_route("/kickoff", self.kickoff_crew, methods=["POST"])

        self.router.add_api_route("/crews", self.read_all, methods=["GET"])
        self.router.add_api_route("/crew/{crew_id}", self.get, methods=["GET"])
        self.router.add_api_route("/crew", self.create, methods=["POST"])
        self.router.add_api_route("/crew/{crew_id}", self.update, methods=["PUT"])
        self.router.add_api_route("/crew/{crew_id}", self.delete, methods=["DELETE"])

    async def kickoff_crew(self, crew_id: UUID4) -> dict:
        crew_response = await self.crew_service.kickoff_crew(CrewEntity(crew_id))
        return {
            "message": crew_response.raw,
            "crew": crew_id
        }

    async def read_all(self) -> list[CrewDto]:
        return await self.crew_service.read_all()

    async def get(self, crew_id: UUID4) -> CrewDto:
        return await self.crew_service.read(crew_id)

    async def create(self, crew: CrewDto) -> CrewDto:
        return await self.crew_service.create(crew)

    async def update(self, crew_id: UUID4, crew: CrewDto) -> CrewDto:
        return await self.crew_service.update(crew_id, crew)

    async def delete(self, crew_id: UUID4) -> bool:
        return await self.crew_service.delete(crew_id)
