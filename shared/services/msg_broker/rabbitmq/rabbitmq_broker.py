from typing import Any, Dict, Optional, Callable, Awaitable

import aio_pika

from core.services.core import settings
from shared.services.msg_broker import AbstractMessageBroker


class RabbitMQMessageBroker(AbstractMessageBroker):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None
        self.exchange = None
        self._callbacks = {}

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(
            f"amqp://{self.username}:{self.password}@{self.host}:{self.port}/"
        )
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            settings.msg_broker.rabbitmq.exchange,
            settings.msg_broker.rabbitmq.exchange_type,
            durable=True,
        )

    async def disconnect(self) -> None:
        if self.connection:
            await self.connection.close()

    async def publish(self, channel: str, message: Dict[str, Any]) -> bool:
        if not self.connection:
            await self.connect()

        message = aio_pika.Message(
            body=self.serialize(message).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await self.exchange.publish(message, routing_key=channel)
        return True

    async def check_subscription(self, channel: str) -> bool:
        if not self.connection:
            await self.connect()

        try:
            return (
                bool(await self.channel.get_queue(channel))
                and channel in self._callbacks
            )
        except aio_pika.exceptions.ChannelClosed:
            return False

    async def subscribe(
        self, channel: str, callback: Callable[[Any], Awaitable[None]]
    ) -> None:
        if not self.connection:
            await self.connect()

        queue = await self.channel.declare_queue(channel, durable=True)
        await queue.bind(self.exchange, routing_key=channel)

        self._callbacks[channel] = callback
        await queue.consume(self._create_message_handler(channel))

    async def unsubscribe(self, channel: str) -> None:
        if channel in self._callbacks:
            del self._callbacks[channel]
            queue = await self.channel.get_queue(channel)
            if queue:
                await queue.delete()

    def _create_message_handler(self, channel: str):
        async def handler(message: aio_pika.IncomingMessage):
            async with message.process():
                data = self.deserialize(message.body.decode())
                if channel in self._callbacks:
                    await self._callbacks[channel](data)

        return handler

    async def get(self, key: str) -> Optional[Any]:
        if not self.connection:
            await self.connect()

        queue = await self.channel.declare_queue(key, durable=True)
        message = await queue.get()
        if message:
            await message.ack()
            return self.deserialize(message.body.decode())
        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        if not self.connection:
            await self.connect()

        message = aio_pika.Message(
            body=self.serialize(value).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        if ttl is not None:
            message.expiration = ttl * 1000

        await self.exchange.publish(message, routing_key=key)
        return True

    async def delete(self, key: str) -> bool:
        if not self.connection:
            await self.connect()

        queue = await self.channel.declare_queue(key, durable=True)
        await queue.delete()
        return True

    async def exists(self, key: str) -> bool:
        try:
            queue = await self.channel.declare_queue(key, passive=True)
            if queue:
                return True
            return False
        except aio_pika.exceptions.ChannelClosed:
            return False

    async def get_all(self, pattern: str) -> Dict[str, Any]:
        result = {}
        try:
            queue = await self.channel.declare_queue(pattern, passive=True)
            message = await queue.get()
            if message:
                await message.ack()
                result[pattern] = self.deserialize(message.body.decode())
        except aio_pika.exceptions.ChannelClosed:
            pass
        return result
