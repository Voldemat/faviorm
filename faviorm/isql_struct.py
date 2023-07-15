from abc import ABC, abstractmethod
from typing import Iterable

from .ihasher import IHasher


class ISqlStruct(ABC):
    @abstractmethod
    def get_sql_hash(self, hasher: IHasher) -> bytes:
        pass


def map_get_sql_hash(
    hasher: IHasher, structs: Iterable[ISqlStruct]
) -> Iterable[bytes]:
    return map(lambda s: s.get_sql_hash(hasher), structs)
