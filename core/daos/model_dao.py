from core.daos.base_dao import BaseDao
from core.dtos.model.model_dto import ModelDto
from core.repositories.model_repository import ModelRepository
from core.repositories.schemas.model_schema import ModelSchema


class ModelDao(BaseDao[ModelDto, ModelSchema]):
    def __init__(self, model_repository: ModelRepository) -> None:
        super().__init__(model_repository)
        self.dto = ModelDto
        self.schema = ModelSchema
