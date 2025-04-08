from fastapi import APIRouter
from pydantic import UUID4

from core.controllers.base_controller import BaseController
from core.dtos.relation import RelationDto


class RelationController(BaseController):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(tags=self.relation_swagger_tags)

        self.router.add_api_route("/relations", self.read_all, methods=["GET"])
        self.router.add_api_route("/relation/{relation_id}", self.get, methods=["GET"])
        self.router.add_api_route("/relation", self.create, methods=["POST"])
        self.router.add_api_route(
            "/relation/{relation_id}", self.update, methods=["PUT"]
        )
        self.router.add_api_route(
            "/relation/{relation_id}", self.delete, methods=["DELETE"]
        )

    async def read_all(self) -> list[RelationDto]:
        return await self.relation_service.read_all()

    async def get(self, relation_id: UUID4) -> RelationDto:
        return await self.relation_service.read(relation_id)

    async def create(self, relation: RelationDto) -> RelationDto:
        return await self.relation_service.create(relation)

    async def update(self, relation_id: UUID4, relation: RelationDto) -> RelationDto:
        return await self.relation_service.update(relation_id, relation)

    async def delete(self, relation_id: UUID4) -> bool:
        return await self.relation_service.delete(relation_id)
