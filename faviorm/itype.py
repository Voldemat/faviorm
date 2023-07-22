from .ihasher import IHasher
from .isql_struct import ISqlStruct


class IType(ISqlStruct):
    def get_params_hash(self, hasher: IHasher) -> bytes:
        return self.get_sql_hash(hasher)
