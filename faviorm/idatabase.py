from abc import abstractmethod

from .ihasher import IHasher
from .isql_struct import ISqlStruct, map_get_sql_hash
from .itable import ITable


class IDatabase(ISqlStruct):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_tables(self) -> list[ITable]:
        pass

    def get_sql_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(
            [self.get_name().encode(), self.get_params_hash(hasher)]
        )

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(list(map_get_sql_hash(hasher, self.get_tables())))
