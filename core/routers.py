from fastapi import APIRouter

from core.controllers.agent_controller import AgentController
from core.controllers.crew_controller import CrewController
from core.controllers.flow_engine_controller import FlowEngineController
from core.controllers.model_controller import ModelController
from core.controllers.prompt_controller import PromptController
from core.controllers.relation_controller import RelationController
from core.controllers.task_controller import TaskController

routes: list[APIRouter] = [
    AgentController().router,
    PromptController().router,
    TaskController().router,
    ModelController().router,
    RelationController().router,
    CrewController().router,
    FlowEngineController().router,
]
