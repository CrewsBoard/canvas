from pydantic import BaseModel


class DatabaseSettingsDto(BaseModel):
    url: str
    schema_package: str
