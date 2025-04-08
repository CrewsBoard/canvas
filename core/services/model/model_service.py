from crewai import LLM
from pydantic import validate_call

from core.daos import ModelDao
from core.dtos.entity.model_entity import ModelEntity
from core.dtos.model import ModelDto
from core.repositories import ModelRepository
from core.services.core import BaseService


class ModelService(BaseService[ModelDto, LLM]):
    def __init__(self):
        self.model_dao = ModelDao(
            ModelRepository(),
        )
        super().__init__(self.model_dao)

    @validate_call
    async def build(self, entity: ModelEntity):
        model_entity = await self.read(entity.id)
        if model_entity is None:
            raise Exception(f"Model {entity.id} not found")
        return LLM(
            model=f"{model_entity.provider}/{model_entity.name}",
            api_key=model_entity.api_key,
            base_url=model_entity.connection_url,
        )
