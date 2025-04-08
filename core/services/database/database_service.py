import importlib
import inspect
import os
from contextlib import asynccontextmanager
from typing import List

from overrides import overrides
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from sqlmodel import SQLModel

from core.services.core import settings
from core.services.database.abstract_database_service import AbstractDatabaseService
from shared.utils import logger
from shared.utils.funcs import get_root_path, get_project_name


class DatabaseService(AbstractDatabaseService):
    _illegal_schema_files = [
        "__init__.py",
        "base_schema.py",
    ]

    _illegal_schema_classes = [
        "BaseSchema",
    ]

    def __init__(self):
        self._engine = self._create_engine()
        self._session_factory = async_sessionmaker(self._engine, expire_on_commit=False)

    @asynccontextmanager
    async def session(self):
        async with self._session_factory() as session:
            try:
                yield session
            except Exception as e:
                logger.error("Error during session: %s", e)
                await session.rollback()
                raise
            finally:
                await session.close()

    @overrides
    async def init_database(self) -> None:
        await self._create_database(self._engine)

    @overrides
    async def dispose(self) -> None:
        await self._engine.dispose()

    @staticmethod
    def _create_engine() -> AsyncEngine:
        try:
            return create_async_engine(settings.database.url, echo=True)
        except Exception as e:
            logger.error(f"Error creating engine: {e}")
            raise e

    async def _create_database(self, engine: AsyncEngine) -> None:
        logger.info(f"Creating database schema for {settings.database.schema_package}")
        try:
            schema_package = settings.database.schema_package
            schema_package = schema_package.replace(f"{get_project_name()}.", "")
            schema_package_split = os.sep.join(schema_package.split("."))
            schema_package_path = os.path.join(get_root_path(), schema_package_split)
            if not os.path.exists(schema_package_path):
                raise FileNotFoundError(
                    f"Schema package path does not exist: {schema_package_path}"
                )
            schema_package_files = os.listdir(schema_package_path)
            schema_package_files = [
                file
                for file in schema_package_files
                if file.endswith(".py") and file not in self._illegal_schema_files
            ]
            schema_packages = [
                ".".join([settings.database.schema_package, file.split(".")[0]])
                for file in schema_package_files
            ]

            async def load_schemas():
                _schemas: List[type[SQLModel]] = []
                for module_name in schema_packages:
                    try:
                        module = importlib.import_module(module_name)
                        for name, obj in inspect.getmembers(module):
                            if name in self._illegal_schema_classes:
                                continue
                            if (
                                inspect.isclass(obj)
                                and issubclass(obj, SQLModel)
                                and getattr(obj, "__tablename__", None)
                            ):
                                _schemas.append(obj)
                    except Exception as e:
                        print(f"Error loading module {module_name}: {e}")
                return _schemas

            schemas = await load_schemas()
            async with self._engine.begin() as conn:
                await conn.run_sync(
                    SQLModel.metadata.create_all,
                    tables=[
                        table.__table__ for table in schemas if table is not SQLModel
                    ],
                )
            logger.info("Database schema created successfully.")
        except Exception as e:
            logger.error(f"Error creating database schema: {e}")
            raise e
