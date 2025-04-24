from aio_pika import ExchangeType
from pydantic import BaseModel


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
    redis: RedisSettingsDto
    rabbitmq: RabbitMQSettingsDto
