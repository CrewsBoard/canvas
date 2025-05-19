from core.daos.base_dao import BaseDao
from core.dtos.agent.agent_dto import AgentDto
from core.repositories.agent_repository import AgentRepository
from core.repositories.schemas.agent_schema import AgentSchema


class AgentDao(BaseDao[AgentDto, AgentSchema]):
    def __init__(self, prompt_repository: AgentRepository) -> None:
        super().__init__(prompt_repository)
        self.dto = AgentDto
        self.schema = AgentSchema
