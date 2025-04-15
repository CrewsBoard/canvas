from core.repositories.base_repository import BaseRepository
from core.repositories.schemas.agent_schema import AgentSchema
from shared.services.database import database_service


class AgentRepository(BaseRepository[AgentSchema]):
    def __init__(self):
        super().__init__(database_service)
        self.schema = AgentSchema
