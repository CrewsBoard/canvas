from core.repositories.base_repository import BaseRepository
from core.repositories.schemas.model_schema import ModelSchema
from shared.services.database import database_service


class ModelRepository(BaseRepository[ModelSchema]):
    def __init__(self):
        super().__init__(database_service)
        self.schema = ModelSchema
