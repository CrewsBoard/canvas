from core.repositories.base_repository import BaseRepository
from core.repositories.schemas.agent_schema import AgentSchema
from core.services.database import database_service


class AgentRepository(BaseRepository[AgentSchema]):
    def __init__(self):
        super().__init__(database_service)
        self.schema = AgentSchema
