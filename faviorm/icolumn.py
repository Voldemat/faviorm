from abc import abstractmethod

from .ihasher import IHasher
from .isql_struct import ISqlStruct
from .itype import IType


class IColumn(ISqlStruct):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_type(self) -> IType:
        pass

    def get_sql_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(
            [self.get_name().encode(), self.get_params_hash(hasher)]
        )

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return self.get_type().get_sql_hash(hasher)
