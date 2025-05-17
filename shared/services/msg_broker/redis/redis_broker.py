from typing import Any, Dict, Optional, Callable, Awaitable

import redis.asyncio as redis

from shared.services.msg_broker import AbstractMessageBroker


class RedisMessageBroker(AbstractMessageBroker):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        password: Optional[str],
    ):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.redis = None
        self.pubsub = None
        self._callbacks = {}

    async def connect(self) -> None:
        self.redis = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=True,
            socket_timeout=5,
            socket_connect_timeout=5,
            retry_on_timeout=True,
        )
        self.pubsub = self.redis.pubsub()
        await self.redis.ping()

    async def disconnect(self) -> None:
        if self.pubsub:
            await self.pubsub.close()
        if self.redis:
            await self.redis.close()

    async def publish(self, channel: str, message: Dict[str, Any]) -> bool:
        if not self.redis:
            await self.connect()
        try:
            serialized = self.serialize(message)
            return bool(await self.redis.publish(channel, serialized))
        except redis.ConnectionError:
            await self.connect()
            serialized = self.serialize(message)
            return bool(await self.redis.publish(channel, serialized))

    async def check_subscription(self, channel: str) -> bool:
        if not self.redis:
            await self.connect()
        try:
            return (
                bool(await self.redis.pubsub().channels.get(channel))
                and channel in self._callbacks
            )
        except redis.ConnectionError:
            return False

    async def subscribe(
        self, channel: str, callback: Callable[[Any], Awaitable[None]]
    ) -> None:
        if not self.pubsub:
            await self.connect()
        self._callbacks[channel] = callback
        await self.pubsub.subscribe(channel)
        await self._listen()

    async def unsubscribe(self, channel: str) -> None:
        if not self.pubsub:
            return
        if channel in self._callbacks:
            del self._callbacks[channel]
        await self.pubsub.unsubscribe(channel)

    async def _listen(self) -> None:
        while True:
            try:
                message = await self.pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    channel = message["channel"]
                    data = self.deserialize(message["data"])
                    if channel in self._callbacks:
                        await self._callbacks[channel](data)
            except redis.ConnectionError:
                await self.connect()

    async def get(self, key: str) -> Optional[Any]:
        if not self.redis:
            await self.connect()
        try:
            value = await self.redis.get(key)
            if value is None:
                return None
            return self.deserialize(value)
        except redis.ConnectionError:
            await self.connect()
            value = await self.redis.get(key)
            if value is None:
                return None
            return self.deserialize(value)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        if not self.redis:
            await self.connect()
        try:
            serialized = self.serialize(value)
            if ttl is not None:
                return bool(await self.redis.setex(key, ttl, serialized))
            return bool(await self.redis.set(key, serialized))
        except redis.ConnectionError:
            await self.connect()
            serialized = self.serialize(value)
            if ttl is not None:
                return bool(await self.redis.setex(key, ttl, serialized))
            return bool(await self.redis.set(key, serialized))

    async def delete(self, key: str) -> bool:
        if not self.redis:
            await self.connect()
        try:
            return bool(await self.redis.delete(key))
        except redis.ConnectionError:
            await self.connect()
            return bool(await self.redis.delete(key))

    async def exists(self, key: str) -> bool:
        if not self.redis:
            await self.connect()
        try:
            return bool(await self.redis.exists(key))
        except redis.ConnectionError:
            await self.connect()
            return bool(await self.redis.exists(key))

    async def get_all(self, pattern: str) -> Dict[str, Any]:
        if not self.redis:
            await self.connect()
        try:
            keys = await self.redis.keys(pattern)
            result = {}
            for key in keys:
                value = await self.get(key)
                if value is not None:
                    result[key] = value
            return result
        except redis.ConnectionError:
            await self.connect()
            keys = await self.redis.keys(pattern)
            result = {}
            for key in keys:
                value = await self.get(key)
                if value is not None:
                    result[key] = value
            return result
