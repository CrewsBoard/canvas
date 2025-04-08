from core.daos.base_dao import BaseDao
from core.dtos.prompt import PromptDto
from core.repositories import PromptRepository
from core.repositories.schemas.prompt_schema import PromptSchema


class PromptDao(BaseDao[PromptDto, PromptSchema]):
    def __init__(self, prompt_repository: PromptRepository):
        super().__init__(prompt_repository)
        self.dto = PromptDto
        self.schema = PromptSchema
