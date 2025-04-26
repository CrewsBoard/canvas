import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Callable, Awaitable

from pydantic import BaseModel


class AbstractMessageBroker(ABC):
    """Abstract base class for message brokers."""

    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the message broker."""
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection to the message broker."""
        raise NotImplementedError

    @abstractmethod
    async def publish(self, channel: str, message: Any) -> bool:
        """Publish a message to a channel."""
        raise NotImplementedError

    @abstractmethod
    async def subscribe(
        self, channel: str, callback: Callable[[Any], Awaitable[None]]
    ) -> None:
        """Subscribe to a channel and register a callback."""
        raise NotImplementedError

    @abstractmethod
    async def unsubscribe(self, channel: str) -> None:
        """Unsubscribe from a channel."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from the state store."""
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set a value in the state store with optional TTL."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete a value from the state store."""
        raise NotImplementedError

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if a key exists in the state store."""
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, pattern: str) -> Dict[str, Any]:
        """Get all values matching a pattern."""
        raise NotImplementedError

    @staticmethod
    def serialize(value: Any) -> str:
        """Serialize a value to a string."""
        if isinstance(value, str):
            return value
        if isinstance(value, BaseModel):
            return value.model_dump_json()
        return json.dumps(value)

    @staticmethod
    def deserialize(value: str) -> Any:
        """Deserialize a string to a value."""
        return json.loads(value)
