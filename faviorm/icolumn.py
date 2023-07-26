from abc import abstractmethod

from .ihasher import IHasher
from .isql_struct import ISqlStruct
from .itype import IType


class IColumn(ISqlStruct):
    @abstractmethod
    def get_type(self) -> IType:
        pass

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return self.get_type().get_sql_hash(hasher)
