from pydantic import BaseModel

from shared.dtos.database import DatabaseTypes


class DatabaseSettingsDto(BaseModel):
    driver: str
    type: DatabaseTypes
    host: str
    port: int
    db_name: str
    username: str
    password: str
    schema_package: str
