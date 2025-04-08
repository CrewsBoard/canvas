from core.services.agent.agent_service import AgentService
from core.services.crew.crew_service import CrewService
from core.services.model.model_service import ModelService
from core.services.prompt.prompt_service import PromptService
from core.services.relation.relation_service import RelationService
from core.services.task.task_service import TaskService


class BaseController:
    def __init__(self):
        self.prompt_swagger_tags = ["Prompt"]
        self.prompt_service: PromptService = PromptService()

        self.agent_swagger_tags = ["Agent"]
        self.agent_service: AgentService = AgentService(
            RelationService(), ModelService(), PromptService()
        )

        self.model_swagger_tags = ["Model"]
        self.model_service: ModelService = ModelService()

        self.relation_swagger_tags = ["Relation"]
        self.relation_service: RelationService = RelationService()

        self.task_swagger_tags = ["Task"]
        self.task_service: TaskService = TaskService(
            AgentService(RelationService(), ModelService(), PromptService()),
            RelationService(),
            PromptService(),
        )

        self.crew_swagger_tags = ["Crew"]
        self.crew_service: CrewService = CrewService(
            AgentService(RelationService(), ModelService(), PromptService()),
            TaskService(
                AgentService(RelationService(), ModelService(), PromptService()),
                RelationService(),
                PromptService(),
            ),
            RelationService(),
        )
