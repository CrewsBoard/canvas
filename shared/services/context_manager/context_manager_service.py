from core.services.agent.agent_service import AgentService
from core.services.crew.crew_service import CrewService
from core.services.flow_engine.flow_engine_service import FlowEngineService
from core.services.model.model_service import ModelService
from core.services.prompt.prompt_service import PromptService
from core.services.relation.relation_service import RelationService
from core.services.task.task_service import TaskService
from shared.dtos.msg_broker import MsgBrokerTypes
from shared.services.msg_broker import MessageBrokerService, AbstractMessageBroker


class ContextManager:
    _initialized = False
    _caching_service = None
    _msg_broker_service = None
    _prompt_service = None
    _agent_service = None
    _model_service = None
    _relation_service = None
    _task_service = None
    _crew_service = None
    _flow_engine_service = None

    @classmethod
    async def initialize(cls):
        if not cls._initialized:
            cls._prompt_service = PromptService()
            cls._agent_service = AgentService(
                cls._relation_service, cls._model_service, cls._prompt_service
            )
            cls._model_service = ModelService()
            cls._relation_service = RelationService()
            cls._task_service = TaskService(
                cls._agent_service, cls._relation_service, cls._prompt_service
            )
            cls._crew_service = CrewService(
                cls._agent_service, cls._task_service, cls._relation_service
            )

            cls._caching_service = await MessageBrokerService.get_instance(
                MsgBrokerTypes.REDIS
            )
            cls._msg_broker_service = await MessageBrokerService.get_instance()

            cls._flow_engine_service = FlowEngineService(
                cls._caching_service,
            )
            cls._initialized = True

    @property
    def prompt_service(self) -> PromptService:
        return type(self)._prompt_service

    @property
    def agent_service(self) -> AgentService:
        return type(self)._agent_service

    @property
    def model_service(self) -> ModelService:
        return type(self)._model_service

    @property
    def relation_service(self) -> RelationService:
        return type(self)._relation_service

    @property
    def task_service(self) -> TaskService:
        return type(self)._task_service

    @property
    def crew_service(self) -> CrewService:
        return type(self)._crew_service

    @property
    def flow_engine_service(self) -> FlowEngineService:
        return type(self)._flow_engine_service

    @property
    def caching_service(self) -> AbstractMessageBroker:
        return type(self)._caching_service

    @property
    def msg_broker_service(self) -> AbstractMessageBroker:
        return type(self)._msg_broker_service
