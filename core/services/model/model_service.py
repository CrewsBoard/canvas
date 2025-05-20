from crewai import LLM
from pydantic import validate_call

from core.daos.model_dao import ModelDao
from core.dtos.entity.model_entity import ModelEntity
from core.dtos.model.model_dto import ModelDto
from core.repositories.model_repository import ModelRepository
from core.services.core.base_service import BaseService


class ModelService(BaseService[ModelDto, LLM]):
    def __init__(self):
        self.model_dao = ModelDao(
            ModelRepository(),
        )
        super().__init__(self.model_dao)

    @validate_call
    async def build(self, entity: ModelEntity):
        # @todo handle model_id=None with is_default prop
        model_entity = await self.read(entity.id)
        if model_entity is None:
            raise Exception(f"Model {entity.id} not found")
        return LLM(
            model=f"{model_entity.provider}/{model_entity.name}",
            api_key=model_entity.api_key,
            base_url=model_entity.connection_url,
        )
