from typing import List, Dict

from crewai import Crew
from crewai.crews import CrewOutput

from core.daos import CrewDao
from core.dtos.crew import CrewDto
from core.dtos.entity.agent_entity import AgentEntity
from core.dtos.entity.crew_entity import CrewEntity
from core.dtos.entity.task_entity import TaskEntity
from core.dtos.relation.relation_direction import RelationDirection
from core.repositories import CrewRepository
from core.services.agent.agent_service import AgentService
from core.services.core import BaseService
from core.services.relation.relation_service import RelationService
from core.services.task.task_service import TaskService
from shared.utils import logger


class CrewService(BaseService[CrewDto, Crew]):
    crews: Dict[str, Crew] = {}

    def __init__(
        self,
        agent_service: AgentService,
        task_service: TaskService,
        relation_service: RelationService,
    ):
        self.crew_dao = CrewDao(CrewRepository())
        self.agent_service = agent_service
        self.task_service = task_service
        self.relation_service = relation_service
        super().__init__(self.crew_dao)

    async def build(self, entity: CrewEntity):
        crew_entity = await self.read(entity.id)
        agent_entities: List[AgentEntity] = (
            await self.relation_service.get_related_entities(
                entity, RelationDirection.TO, AgentEntity
            )
        )
        agents = await self.agent_service.build_all(agent_entities)
        task_entities = await self.relation_service.get_related_entities(
            entity, RelationDirection.TO, TaskEntity
        )
        tasks = await self.task_service.build_all(task_entities)
        return Crew(
            name=crew_entity.name,
            agents=agents,
            tasks=tasks,
            process=crew_entity.process,
            verbose=True,
        )

    async def build_all(self, entities=list[CrewEntity]):
        raise NotImplementedError()

    async def kickoff_crew(self, entity: CrewEntity) -> CrewOutput:
        logger.info(f"Kickoff agent id: {entity}")
        crew = await self.build(entity)
        return await crew.kickoff_async()
