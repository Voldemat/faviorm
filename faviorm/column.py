from dataclasses import dataclass
from typing import Literal

from .icolumn import IColumn
from .ihasher import IHasher
from .inullable import INullable
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
class Nullable(INullable):
    nullable: bool

    def get_name(self) -> str:
        return "Nullable"

    def __hash__(self) -> int:
        return hash(self.nullable)

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(bytes(self.nullable))


@dataclass
class Column(IColumn):
    name: str
    type: IType
    nullable: INullable

    def __hash__(self) -> int:
        return hash((self.name, self.type, self.nullable))

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> IType:
        return self.type

    def get_is_nullable(self) -> INullable:
        return self.nullable
