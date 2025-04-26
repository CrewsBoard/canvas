from aio_pika import ExchangeType
from pydantic import BaseModel

from shared.dtos.msg_broker import MsgBrokerTypes


class RedisSettingsDto(BaseModel):
    host: str
    port: int
    db: int
    password: str


class RabbitMQSettingsDto(BaseModel):
    host: str
    port: int
    username: str
    password: str
    exchange: str
    exchange_type: ExchangeType


class MsgBrokerSettingsDto(BaseModel):
    active: MsgBrokerTypes
    redis: RedisSettingsDto
    rabbitmq: RabbitMQSettingsDto
