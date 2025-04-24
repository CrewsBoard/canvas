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


class MsgBrokerSettingsDto(BaseModel):
    redis: RedisSettingsDto
    rabbitmq: RabbitMQSettingsDto
