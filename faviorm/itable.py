from abc import abstractmethod

from .icolumn import IColumn
from .ihasher import IHasher
from .isql_struct import ISqlStruct, map_get_sql_hash


class ITable(ISqlStruct):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_columns(self) -> list[IColumn]:
        pass

    def get_sql_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(
            [
                self.get_name().encode(),
                *list(map_get_sql_hash(hasher, self.get_columns())),
            ]
        )
