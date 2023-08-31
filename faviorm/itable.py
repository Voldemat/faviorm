from abc import abstractmethod

from .icolumn import IColumn
from .ihasher import IHasher
from .isql_struct import ISqlStruct, T, map_get_sql_hash


class ITable(ISqlStruct):
    @abstractmethod
    def get_columns(self) -> list[IColumn[T]]:
        pass

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(list(map_get_sql_hash(hasher, self.get_columns())))
