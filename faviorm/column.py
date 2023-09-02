from dataclasses import dataclass
from typing import Literal

from .icolumn import IColumn
from .ihasher import IHasher
from .itype import IType


class UUID(IType):
    def get_name(self) -> Literal["UUID"]:
        return "UUID"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


@dataclass
class VARCHAR(IType):
    max_length: int

    def get_name(self) -> Literal["VARCHAR"]:
        return "VARCHAR"

    def __hash__(self) -> int:
        return hash((self.get_name(), self.max_length))

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(str(self.max_length).encode())


@dataclass
class Column(IColumn):
    name: str
    type: IType
    nullable: bool

    def __hash__(self) -> int:
        return hash((self.name, self.type, self.nullable))

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> IType:
        return self.type

    def get_is_nullable(self) -> bool:
        return self.nullable
