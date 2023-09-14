from abc import ABC, abstractmethod
from typing import Any, Iterable, Protocol, Sequence

from .idatabase import IDatabase


class ISQLQueryResult(Protocol, Iterable[Any]):
    def __getitem__(self, index: int) -> Any:
        pass

    def get(self, key: str) -> Any:
        pass

    def __next__(self) -> Any:
        pass


class ISQLLoaderExecutor(ABC):
    @abstractmethod
    async def execute(
        self, query: str, args: Sequence[Any] = []
    ) -> list[ISQLQueryResult]:
        pass


class ISQLLoader:
    @abstractmethod
    async def load(self) -> IDatabase:
        pass
