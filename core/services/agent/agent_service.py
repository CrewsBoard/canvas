from typing import Optional, List, Dict

from crewai import Agent
from pydantic import validate_call

from core.daos import AgentDao
from core.dtos.agent import AgentDto
from core.dtos.entity.agent_entity import AgentEntity
from core.dtos.entity.model_entity import ModelEntity
from core.dtos.entity.prompt_entity import PromptEntity
from core.dtos.prompt import PromptDto, PromptTypes
from core.dtos.relation.relation_direction import RelationDirection
from core.repositories import AgentRepository
from core.services.core import BaseService
from core.services.model.model_service import ModelService
from core.services.prompt.prompt_service import PromptService
from core.services.relation.relation_service import RelationService


class AgentService(BaseService[AgentDto, Agent]):
    agent_flows: Dict[str, List["AgentFlow"]] = {}

    def __init__(
        self,
        relation_service: RelationService,
        model_service: ModelService,
        prompt_service: PromptService,
    ):
        self.agent_dao = AgentDao(AgentRepository())
        self.relation_service = relation_service
        self.model_service = model_service
        self.prompt_service = prompt_service
        super().__init__(self.agent_dao)

    @validate_call
    async def build(self, entity: AgentEntity):
        llm = None
        agent_entity_details = await self.read(entity.id)
        if agent_entity_details is None:
            raise Exception(f"Agent {entity.id} not found")
        if agent_entity_details.llm_id is not None:
            llm = await self.model_service.build(
                ModelEntity(agent_entity_details.llm_id)
            )
        prompt_entities: List[PromptEntity] = (
            await self.relation_service.get_related_entities(
                entity, RelationDirection.TO, PromptEntity
            )
        )
        prompt_details: list[PromptDto] = await self.prompt_service.read_by_ids(
            prompt_entities
        )
        if len(prompt_details) != 3:
            raise Exception("Task must have exactly 3 prompts")
        return Agent(
            role=[
                prompt for prompt in prompt_details if prompt.type == PromptTypes.ROLE
            ][0].value,
            goal=[
                prompt for prompt in prompt_details if prompt.type == PromptTypes.GOAL
            ][0].value,
            backstory=[
                prompt
                for prompt in prompt_details
                if prompt.type == PromptTypes.BACKSTORY
            ][0].value,
            llm=llm,
            verbose=agent_entity_details.verbose,
        )

    async def build_all(self, entities: Optional[List[AgentEntity]]):
        if entities is None:
            agents_entities = [AgentEntity(agent.id) for agent in await self.read_all()]
        else:
            agents_entities = [AgentEntity(agent.id) for agent in entities]
        agents: List[Agent] = []
        for entity in agents_entities:
            agent = await self.build(entity)
            agents.append(agent)
        return agents
