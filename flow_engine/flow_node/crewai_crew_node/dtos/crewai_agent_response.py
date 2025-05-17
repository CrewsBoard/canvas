from pydantic import BaseModel


class CrewaiAgentResponse(BaseModel):
    output: str
    is_valid: bool
