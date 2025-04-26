from typing import List, Dict, Any

from pydantic import BaseModel


class FlowEngineEventFactory(BaseModel):
    traversed_node: List[str] = []
    message: Dict[str, Dict[str, Any]] = {}
