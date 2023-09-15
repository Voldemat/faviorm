from dataclasses import dataclass

from .icolumn import IColumn
from .isql_struct import PType
from .itype import IType


@dataclass
class Column(IColumn[PType]):
    name: str
    type: IType[PType]
    nullable: bool
    default: PType | None = None

    def __hash__(self) -> int:
        return hash((self.name, self.type, self.nullable, self.default))

    def get_default_value_hash(self) -> bytes:
        if type(self.default) is str:
            return self.default.encode()
        return bytes()

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> IType[PType]:
        return self.type

    def get_is_nullable(self) -> bool:
        return self.nullable

    def get_default(self) -> PType | None:
        return self.default
