import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.services.core.bootstrapper_service import BootstrapperService


def create_app():
    async def startup():
        await BootstrapperService.start(app)

    async def shutdown():
        await BootstrapperService.stop(app)

    app = FastAPI(docs_url="/docs", redoc_url="/redoc",
                  swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})
    app.add_event_handler('startup', startup)
    app.add_event_handler('shutdown', shutdown)
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


if __name__ == "__main__":
    server_config = uvicorn.Config(app=create_app(), host="0.0.0.0", port=8000, reload=True)
    server = uvicorn.Server(server_config)
    server.run()
