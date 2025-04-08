from typing import Optional, List, TypeVar, Generic

from pydantic import UUID4

from core.dtos.entity.entity import Entity

DtoType = TypeVar("DtoType")
T = TypeVar("T")


class BaseService(Generic[DtoType, T]):
    def __init__(self, dao):
        self.dao = dao

    async def create(self, dto: DtoType) -> DtoType:
        return await self.dao.create(dto)

    async def read(self, schema_id: UUID4) -> Optional[DtoType]:
        return await self.dao.read(schema_id)

    async def update(self, schema_id: UUID4, dto: DtoType) -> Optional[DtoType]:
        return await self.dao.update(schema_id, dto)

    async def delete(self, schema_id: UUID4) -> bool:
        return await self.dao.delete(schema_id)

    async def read_all(self) -> List[DtoType]:
        return await self.dao.read_all()

    async def read_by_ids(self, ids: List[Entity]) -> List[DtoType]:
        return await self.dao.read_by_ids([_id.id for _id in ids])

    # @todo replace all list with List
    async def build_all(self, entities: Optional[List[Entity]]) -> list[T]:
        raise NotImplementedError()

    async def build(self, entity: Entity) -> T:
        raise NotImplementedError()
