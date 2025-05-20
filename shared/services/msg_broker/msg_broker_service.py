from typing import Dict, Optional

from core.services.core import settings
from shared.dtos.msg_broker.msg_broker_types import MsgBrokerTypes
from shared.services.msg_broker.abstract_msg_broker import AbstractMessageBroker
from shared.services.msg_broker.rabbitmq.rabbitmq_broker import RabbitMQMessageBroker
from shared.services.msg_broker.redis.redis_broker import RedisMessageBroker
from shared.utils.logger import logger


class MessageBrokerService:
    _instances: Dict[str, AbstractMessageBroker] = {}

    @classmethod
    async def get_instance(cls, broker_type: Optional[MsgBrokerTypes] = None) -> AbstractMessageBroker:
        broker_type = broker_type or settings.msg_broker.active or MsgBrokerTypes.REDIS.value
        kwargs = cls._get_args(broker_type)

        key = f"{broker_type}:{kwargs['host']}:{kwargs['port']}"

        if key not in cls._instances:
            if broker_type == MsgBrokerTypes.REDIS:
                cls._instances[key] = RedisMessageBroker(**kwargs)
            elif broker_type == MsgBrokerTypes.RABBITMQ:
                cls._instances[key] = RabbitMQMessageBroker(**kwargs)
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
    async def close(cls, broker_type: str):
        args = cls._get_args(broker_type)
        key = f"{broker_type}:{args['host']}:{args['port']}"
        logger.info(f"Closing message broker instance: {key}")
        if key in cls._instances:
            await cls._instances[key].disconnect()
            del cls._instances[key]
        logger.info(f"Closed message broker instance: {key}")

    @staticmethod
    def _get_args(broker_type: str):
        if broker_type == MsgBrokerTypes.REDIS:
            return {
                "host": settings.msg_broker.redis.host,
                "port": settings.msg_broker.redis.port,
                "db": settings.msg_broker.redis.db,
                "password": settings.msg_broker.redis.password,
            }
        elif broker_type == MsgBrokerTypes.RABBITMQ:
            return {
                "host": settings.msg_broker.rabbitmq.host,
                "port": settings.msg_broker.rabbitmq.port,
                "username": settings.msg_broker.rabbitmq.username,
                "password": settings.msg_broker.rabbitmq.password,
            }
        else:
            raise ValueError(f"Unsupported broker type: {broker_type}")
