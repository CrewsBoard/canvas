from pydantic import BaseModel

from core.dtos.settings.database_types import DatabaseTypes


class DatabaseSettingsDto(BaseModel):
    type: DatabaseTypes = DatabaseTypes.postgresql
    url: str
    schema_package: str
