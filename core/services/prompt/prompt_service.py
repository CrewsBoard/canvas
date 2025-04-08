from core.daos import PromptDao
from core.dtos.prompt import PromptDto
from core.repositories import PromptRepository
from core.services.core import BaseService


class PromptService(BaseService[PromptDto, None]):
    def __init__(self):
        self.prompt_dao = PromptDao(PromptRepository())
        super().__init__(self.prompt_dao)
