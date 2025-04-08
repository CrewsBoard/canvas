from core.daos.base_dao import BaseDao
from core.dtos.model import ModelDto
from core.repositories import ModelRepository
from core.repositories.schemas.model_schema import ModelSchema


class ModelDao(BaseDao[ModelDto, ModelSchema]):
    def __init__(self, model_repository: ModelRepository):
        super().__init__(model_repository)
        self.dto = ModelDto
        self.schema = ModelSchema
