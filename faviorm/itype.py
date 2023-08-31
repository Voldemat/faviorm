from typing import Generic

from .isql_struct import ISqlStruct, T


class IType(ISqlStruct, Generic[T]):
    pass
