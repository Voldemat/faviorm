from abc import abstractmethod

from .ihasher import IHasher
from .isql_struct import ISqlStruct
from .itype import IType


class IColumn(ISqlStruct):
    @abstractmethod
    def get_type(self) -> IType:
        pass

    @abstractmethod
    def get_is_nullable(self) -> bool:
        pass

    def get_nullable_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(bytes(self.get_is_nullable()))

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(
            [
                self.get_type().get_sql_hash(hasher),
                bytes(self.get_is_nullable()),
            ]
        )
