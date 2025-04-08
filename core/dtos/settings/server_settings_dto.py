from pydantic import BaseModel


class ServerSettingsDto(BaseModel):
    name: str = "Default Server"
    debug: bool = False
