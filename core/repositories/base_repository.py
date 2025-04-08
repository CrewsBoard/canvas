from typing import Optional, List, Type, TypeVar, Generic, Dict, Any

from pydantic import UUID4
from sqlmodel import SQLModel, select

SchemaType = TypeVar("SchemaType", bound=SQLModel)


class BaseRepository(Generic[SchemaType]):
    def __init__(self, database_service):
        self.database_service = database_service
        self.schema: Type[SchemaType]

    async def create(self, schema: SchemaType) -> SchemaType:
        async with self.database_service.session() as session:
            session.add(schema)
            await session.commit()
            await session.refresh(schema)
            return schema

    async def read(self, schema_id: UUID4) -> Optional[SchemaType]:
        async with self.database_service.session() as session:
            return await session.get(self.schema, schema_id)

    async def update(
        self, schema_id: UUID4, schema_update: Dict[str, Any]
    ) -> Optional[SchemaType]:
        async with self.database_service.session() as session:
            schema = await session.get(self.schema, schema_id)
            if schema:
                for key, value in schema_update.items():
                    if hasattr(schema, key):
                        if value:
                            setattr(schema, key, value)
                await session.commit()
                await session.refresh(schema)
                return schema
            return None

    async def delete(self, schema_id: UUID4) -> bool:
        async with self.database_service.session() as session:
            schema = await session.get(self.schema, schema_id)
            if schema:
                await session.delete(schema)
                await session.commit()
                return True
            return False

    async def read_all(self) -> List[SchemaType]:
        async with self.database_service.session() as session:
            sql = select(self.schema)
            result = await session.execute(sql)
            schemas = result.scalars().all()
            return list(schemas)

    async def read_by_ids(self, ids: List[UUID4]) -> List[SchemaType]:
        async with self.database_service.session() as session:
            sql = select(self.schema).where(self.schema.id.in_(ids))
            result = await session.execute(sql)
            schemas = result.scalars().all()
            return list(schemas)
