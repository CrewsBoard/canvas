from core.repositories.base_repository import BaseRepository
from core.repositories.schemas.prompt_schema import PromptSchema
from core.services.database import database_service


class PromptRepository(BaseRepository[PromptSchema]):
    def __init__(self):
        super().__init__(database_service)
        self.schema = PromptSchema
