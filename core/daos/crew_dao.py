from core.daos.base_dao import BaseDao
from core.dtos.crew.crew_dto import CrewDto
from core.repositories.crew_repository import CrewRepository
from core.repositories.schemas.crew_schema import CrewSchema


class CrewDao(BaseDao[CrewDto, CrewSchema]):
    def __init__(self, prompt_repository: CrewRepository) -> None:
        super().__init__(prompt_repository)
        self.dto = CrewDto
        self.schema = CrewSchema
