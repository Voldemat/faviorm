from abc import ABC, abstractmethod
from typing import Any, Protocol, Sequence

from .idatabase import IDatabase


class ISQLQueryResult(Protocol):
    def __getitem__(self, index: int) -> Any:
        pass

    def get(self, key: str) -> Any:
        pass


class ISQLLoaderExecutor(ABC):
    @abstractmethod
    async def execute(
        self, query: str, args: Sequence[Any]
    ) -> list[ISQLQueryResult]:
        pass


class ISQLLoader:
    @abstractmethod
    async def load(self) -> IDatabase:
        pass
