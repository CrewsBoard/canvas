from core.repositories.base_repository import BaseRepository
from core.repositories.schemas.crew_schema import CrewSchema
from core.services.database import database_service


class CrewRepository(BaseRepository[CrewSchema]):
    def __init__(self):
        super().__init__(database_service)
        self.schema = CrewSchema
