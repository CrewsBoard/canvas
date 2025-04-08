from fastapi.routing import APIRouter

from core.controllers import AgentController, PromptController, TaskController, ModelController, \
    RelationController, CrewController

routes: list[APIRouter] = [
    AgentController().router,
    PromptController().router,
    TaskController().router,
    ModelController().router,
    RelationController().router,
    CrewController().router,
]
