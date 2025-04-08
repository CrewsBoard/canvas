from typing import List

from crewai import Task

from core.daos.task_dao import TaskDao
from core.dtos.entity.agent_entity import AgentEntity
from core.dtos.entity.prompt_entity import PromptEntity
from core.dtos.entity.task_entity import TaskEntity
from core.dtos.prompt import PromptDto, PromptTypes
from core.dtos.relation.relation_direction import RelationDirection
from core.dtos.task import TaskDto
from core.repositories import TaskRepository
from core.services.agent.agent_service import AgentService
from core.services.core import BaseService
from core.services.prompt.prompt_service import PromptService
from core.services.relation.relation_service import RelationService


class TaskService(BaseService[TaskDto, Task]):
    def __init__(self, agent_service: AgentService, relation_service: RelationService, prompt_service: PromptService):
        self.task_dao = TaskDao(TaskRepository())
        self.agent_service = agent_service
        self.relation_service = relation_service
        self.prompt_service = prompt_service
        super().__init__(self.task_dao)

    async def build(self, entity: TaskEntity):
        task_entity: TaskDto = await self.read(entity.id)
        agent_entities: List[AgentEntity] = await self.relation_service.get_related_entities(entity,
                                                                                             RelationDirection.FROM,
                                                                                             AgentEntity)
        agent = await self.agent_service.build(agent_entities[0]) if len(agent_entities) > 0 else None
        prompt_entities = await self.relation_service.get_related_entities(entity, RelationDirection.TO, PromptEntity)
        prompt_details: list[PromptDto] = await self.prompt_service.read_by_ids(prompt_entities)
        if len(prompt_details) != 2:
            raise Exception("Task must have exactly 2 prompts")
        return Task(
            name=task_entity.name,
            description=[prompt for prompt in prompt_details if prompt.type == PromptTypes.DESCRIPTION][0].value,
            expected_output=[prompt for prompt in prompt_details if prompt.type == PromptTypes.EXPECTED_OUTPUT][
                0].value,
            agent=agent,
        )

    async def build_all(self, entities=list[TaskEntity]):
        tasks: list[Task] = []
        if entities is None:
            tasks_entities = [TaskEntity(task.id) for task in await self.read_all()]
        else:
            tasks_entities = [TaskEntity(task.id) for task in entities]
        for entity in tasks_entities:
            task = await self.build(entity)
            tasks.append(task)
        return tasks

    @staticmethod
    def _required_args(prompt_entities: list[PromptDto]) -> tuple[list[str], list[str]]:
        descriptions = [prompt.value for prompt in prompt_entities if prompt.type == PromptTypes.DESCRIPTION]
        expected_outputs = [prompt.value for prompt in prompt_entities if prompt.type == PromptTypes.EXPECTED_OUTPUT]
        if len(descriptions) != len(expected_outputs):
            raise Exception("Descriptions and expected outputs must be the same length")
        return descriptions, expected_outputs
