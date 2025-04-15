from fastapi import APIRouter

from core.controllers import (
    AgentController,
    PromptController,
    TaskController,
    ModelController,
    RelationController,
    CrewController,
    FlowEngineController,
)

routes: list[APIRouter] = [
    AgentController().router,
    PromptController().router,
    TaskController().router,
    ModelController().router,
    RelationController().router,
    CrewController().router,
    FlowEngineController().router,
]
