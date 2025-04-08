from sqlmodel import select

from core.dtos.entity import EntityType
from core.dtos.entity.entity import Entity
from core.dtos.relation.relation_direction import RelationDirection
from core.repositories.base_repository import BaseRepository
from core.repositories.schemas.relation_schema import RelationSchema
from core.services.database import database_service


class RelationRepository(BaseRepository[RelationSchema]):
    def __init__(self):
        super().__init__(database_service)
        self.schema = RelationSchema

    async def related_entities(self, entity: Entity, direction: RelationDirection, related_with_type: EntityType) -> \
            list[
                RelationSchema]:
        async with self.database_service.session() as session:
            match direction:
                case RelationDirection.FROM:
                    query = select(RelationSchema).where(
                        (RelationSchema.from_entity_id == entity.id) &
                        (RelationSchema.from_entity_type == entity.type) &
                        (RelationSchema.to_entity_type == related_with_type))
                case RelationDirection.TO:
                    query = select(RelationSchema).where(
                        (RelationSchema.to_entity_id == entity.id) &
                        (RelationSchema.to_entity_type == entity.type) &
                        (RelationSchema.from_entity_type == related_with_type))
                case _:
                    raise ValueError("Invalid relation direction")
            result = await session.execute(query)
            return result.scalars().all()
