from typing import Generic

from .isql_struct import ISqlStruct, PType


class IType(ISqlStruct, Generic[PType]):
    pass
