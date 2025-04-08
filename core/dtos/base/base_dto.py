from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4


class BaseDto(BaseModel):
    id: Optional[UUID4] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[UUID4] = None
    updated_by: Optional[UUID4] = None
