from fastapi import FastAPI

from core.routers import routes
from shared.services.database import database_service
from shared.utils import logger


class BootstrapperService:
    @staticmethod
    async def start(app: FastAPI):
        logger.warn("Starting application...")
        await database_service.init_database()
        for route in routes:
            app.include_router(route)
        logger.warn("Application started.")

    @staticmethod
    async def stop(app: FastAPI):
        logger.warn("Stopping application...")
        await database_service.dispose()
        logger.warn("Application stopped.")
