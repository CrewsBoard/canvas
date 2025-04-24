from typing import Optional, Dict

from core.services.core import settings
from shared.dtos.msg_broker import MsgBrokerTypes
from shared.services.msg_broker.abstract_msg_broker import AbstractMessageBroker
from shared.utils import logger
from .rabbitmq.rabbitmq_broker import RabbitMQMessageBroker
from .redis.redis_broker import RedisMessageBroker


class MessageBrokerService:

    _instances: Dict[str, AbstractMessageBroker] = {}

    @classmethod
    async def get_instance(
        cls,
        broker_type: Optional[MsgBrokerTypes] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **kwargs,
    ) -> AbstractMessageBroker:
        broker_type = broker_type or MsgBrokerTypes.REDIS.value
        host = host or settings.msg_broker.redis.host
        port = port or settings.msg_broker.redis.port

        if broker_type == MsgBrokerTypes.REDIS:
            kwargs.setdefault("db", settings.msg_broker.redis.db)
            kwargs.setdefault("password", settings.msg_broker.redis.password)
        elif broker_type == MsgBrokerTypes.RABBITMQ:
            kwargs.setdefault("username", settings.msg_broker.rabbitmq.username)
            kwargs.setdefault("password", settings.msg_broker.rabbitmq.password)

        key = f"{broker_type}:{host}:{port}"

        if key not in cls._instances:
            if broker_type == MsgBrokerTypes.REDIS:
                cls._instances[key] = RedisMessageBroker(host=host, port=port, **kwargs)
            elif broker_type == MsgBrokerTypes.RABBITMQ:
                cls._instances[key] = RabbitMQMessageBroker(
                    host=host, port=port, **kwargs
                )
            else:
                raise ValueError(f"Unsupported broker type: {broker_type}")

            try:
                await cls._instances[key].connect()
                logger.info(f"Connected to message broker: {key}")
            except Exception as e:
                logger.error(f"Error connecting to message broker: {e}")
                raise e

        return cls._instances[key]

    @classmethod
    async def close_all(cls):
        logger.info("Closing all message broker instances...")
        for instance in cls._instances.values():
            await instance.disconnect()
        cls._instances.clear()
        logger.info("All message broker instances closed.")

    @classmethod
    async def close(cls, broker_type: str, host: str, port: int):
        key = f"{broker_type}:{host}:{port}"
        logger.info(f"Closing message broker instance: {key}")
        if key in cls._instances:
            await cls._instances[key].disconnect()
            del cls._instances[key]
        logger.info(f"Closed message broker instance: {key}")
