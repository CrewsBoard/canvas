from typing import Optional, List, TypeVar, Generic, Type

from pydantic import BaseModel, UUID4
from sqlmodel import SQLModel

DtoType = TypeVar("DtoType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=SQLModel)


class BaseDao(Generic[DtoType, SchemaType]):
    def __init__(self, repository):
        self.repository = repository
        self.schema: Type[SchemaType]
        self.dto: Type[DtoType]

    async def create(self, dto: DtoType) -> DtoType:
        schema_object = self.schema(**dto.model_dump())
        data = await self.repository.create(schema_object)
        return self.dto(**data.model_dump())

    async def read(self, schema_id: UUID4) -> Optional[DtoType]:
        data = await self.repository.read(schema_id)
        if data:
            return self.dto(**data.model_dump())
        return None

    async def update(self, schema_id: UUID4, dto: DtoType) -> Optional[DtoType]:
        schema_data = dto.model_dump(exclude_unset=True)
        data = await self.repository.update(schema_id, schema_data)
        if data:
            return self.dto(**data.model_dump())
        return None

    async def delete(self, schema_id: UUID4) -> bool:
        return await self.repository.delete(schema_id)

    async def read_all(self) -> List[DtoType]:
        data = await self.repository.read_all()
        return [self.dto(**item.model_dump()) for item in data]

    async def read_by_ids(self, ids: List[UUID4]) -> List[DtoType]:
        data = await self.repository.read_by_ids(ids)
        return [self.dto(**item.model_dump()) for item in data]
