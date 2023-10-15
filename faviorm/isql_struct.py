from abc import ABC, abstractmethod
from collections.abc import Hashable
from typing import Iterable, TypeVar

from .ihasher import IHasher

PType = TypeVar("PType", covariant=True)


class ISqlStruct(ABC, Hashable):
    @abstractmethod
    def get_name(self) -> str:
        pass

    def get_sql_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(
            [self.get_name().encode(), self.get_params_hash(hasher)]
        )

    @abstractmethod
    def get_params_hash(self, hasher: IHasher) -> bytes:
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ISqlStruct):
            return False

        return hash(self) == hash(other)


def map_get_sql_hash(
    hasher: IHasher, structs: Iterable[ISqlStruct]
) -> Iterable[bytes]:
    return map(lambda s: s.get_sql_hash(hasher), structs)
