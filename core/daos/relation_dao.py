from typing import Generic, List, Type, TypeVar

from core.daos.base_dao import BaseDao
from core.dtos.entity.entity import Entity
from core.dtos.relation.relation_direction import RelationDirection
from core.dtos.relation.relation_dto import RelationDto
from core.repositories.relation_repository import RelationRepository
from core.repositories.schemas.relation_schema import RelationSchema

T = TypeVar("T", bound=Entity)


class RelationDao(BaseDao[RelationDto, RelationSchema], Generic[T]):
    def __init__(self, relation_repository: RelationRepository) -> None:
        super().__init__(relation_repository)
        self.relation_repository = relation_repository
        self.dto = RelationDto
        self.schema = RelationSchema

    async def related_entities(self, entity: Entity, direction: RelationDirection, entity_class: Type[T]) -> List[T]:
        data = await self.relation_repository.related_entities(entity, direction, entity_class.entity_type)
        entity_list: List[T] = []
        for item in data:
            if direction == RelationDirection.FROM:
                entity_list.append(entity_class(item.to_entity_id))
            elif direction == RelationDirection.TO:
                entity_list.append(entity_class(item.from_entity_id))
            else:
                raise ValueError("Invalid relation direction")
        return entity_list
