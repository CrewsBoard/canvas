from core.daos.base_dao import BaseDao
from core.dtos.prompt.prompt_dto import PromptDto
from core.repositories.prompt_repository import PromptRepository
from core.repositories.schemas.prompt_schema import PromptSchema


class PromptDao(BaseDao[PromptDto, PromptSchema]):
    def __init__(self, prompt_repository: PromptRepository) -> None:
        super().__init__(prompt_repository)
        self.dto = PromptDto
        self.schema = PromptSchema
