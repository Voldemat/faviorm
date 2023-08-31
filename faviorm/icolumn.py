from abc import abstractmethod
from typing import Generic

from .ihasher import IHasher
from .isql_struct import ISqlStruct, T
from .itype import IType


class IColumn(ISqlStruct, Generic[T]):
    @abstractmethod
    def get_type(self) -> IType[T]:
        pass

    @abstractmethod
    def get_is_nullable(self) -> bool:
        pass

    @abstractmethod
    def get_default(self) -> T | None:
        pass

    @abstractmethod
    def get_default_value_hash(self) -> bytes:
        pass

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(
            [
                self.get_type().get_sql_hash(hasher),
                bytes(self.get_is_nullable()),
                self.get_default_value_hash(),
            ]
        )
