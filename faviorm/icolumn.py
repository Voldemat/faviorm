from abc import abstractmethod

from .ihasher import IHasher
from .inullable import INullable
from .isql_struct import ISqlStruct, map_get_sql_hash
from .itype import IType


class IColumn(ISqlStruct):
    @abstractmethod
    def get_type(self) -> IType:
        pass

    @abstractmethod
    def get_is_nullable(self) -> INullable:
        pass

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(
            list(
                map_get_sql_hash(
                    hasher, [self.get_is_nullable(), self.get_type()]
                )
            )
        )
