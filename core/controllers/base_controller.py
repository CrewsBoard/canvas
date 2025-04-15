from shared.services.context_manager.context_manager_service import ContextManager


class BaseController(ContextManager):
    def __init__(self):
        super().__init__()

        self.prompt_swagger_tags = ["Prompt"]
        self.agent_swagger_tags = ["Agent"]
        self.model_swagger_tags = ["Model"]
        self.relation_swagger_tags = ["Relation"]
        self.task_swagger_tags = ["Task"]
        self.crew_swagger_tags = ["Crew"]
        self.flow_engine_swagger_tags = ["Flow Engine"]
