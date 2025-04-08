from abc import ABC, abstractmethod


class AbstractDatabaseService(ABC):

    async def session(self):
        raise NotImplementedError()

    @abstractmethod
    async def init_database(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def dispose(self) -> None:
        raise NotImplementedError()
