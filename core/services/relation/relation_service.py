from typing import Generic, List, Type, TypeVar

from core.daos.relation_dao import RelationDao
from core.dtos.entity.entity import Entity
from core.dtos.relation.relation_direction import RelationDirection
from core.dtos.relation.relation_dto import RelationDto
from core.repositories.relation_repository import RelationRepository
from core.services.core.base_service import BaseService

T = TypeVar("T", bound=Entity)


class RelationService(BaseService[RelationDto, None], Generic[T]):
    def __init__(self):
        self.relation_dao = RelationDao(RelationRepository())
        super().__init__(self.relation_dao)

    async def get_related_entities(
        self, entity: Entity, direction: RelationDirection, entity_class: Type[T]
    ) -> List[T]:
        return await self.relation_dao.related_entities(entity, direction, entity_class)
