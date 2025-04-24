from pydantic import BaseModel

from shared.dtos.msg_broker import MsgBrokerTypes


class FlowNodesSettingsDto(BaseModel):
    msg_broker: MsgBrokerTypes
    channel: str
