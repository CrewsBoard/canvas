from fastapi import FastAPI

from core.routers import routes
from flow_engine.flow_chain.services.flow_node_registry_service import FlowNodeRegistry
from shared.services.context_manager.context_manager_service import ContextManager
from shared.services.database import database_service
from shared.services.msg_broker.msg_broker_service import MessageBrokerService
from shared.utils.logger import logger


class BootstrapperService:
    @staticmethod
    async def start(app: FastAPI) -> None:
        logger.warn("Starting application...")
        await database_service.init_database()
        await ContextManager.initialize()
        FlowNodeRegistry.initialize()
        for route in routes:
            app.include_router(route)
        logger.warn("Application started.")

    @staticmethod
    async def stop(app: FastAPI) -> None:
        logger.warn("Stopping application...")
        await database_service.dispose()
        await MessageBrokerService.close_all()
        logger.warn("Application stopped.")
