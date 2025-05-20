from typing import Optional

from core.dtos.base.base_dto import BaseDto
from core.dtos.model.model_types import ModelTypes


class ModelDto(BaseDto):
    name: str
    provider: str
    connection_url: str
    model_type: ModelTypes
    description: Optional[str] = None
    api_key: Optional[str] = None
