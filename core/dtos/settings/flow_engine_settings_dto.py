from pydantic import BaseModel

from shared.dtos.msg_broker import MsgBrokerTypes


class FlowEngineSettingsDto(BaseModel):
    msg_broker: MsgBrokerTypes
    channel: str
