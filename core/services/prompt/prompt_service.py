from core.daos.prompt_dao import PromptDao
from core.dtos.prompt.prompt_dto import PromptDto
from core.repositories.prompt_repository import PromptRepository
from core.services.core.base_service import BaseService


class PromptService(BaseService[PromptDto, None]):
    def __init__(self):
        self.prompt_dao = PromptDao(PromptRepository())
        super().__init__(self.prompt_dao)
