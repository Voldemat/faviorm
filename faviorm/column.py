import uuid
from dataclasses import dataclass
from typing import Generic, Literal

from .icolumn import IColumn
from .ihasher import IHasher
from .isql_struct import T
from .itype import IType


class UUID(IType[uuid.UUID]):
    def get_name(self) -> Literal["UUID"]:
        return "UUID"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


@dataclass
class VARCHAR(IType[str]):
    max_length: int

    def get_name(self) -> Literal["VARCHAR"]:
        return "VARCHAR"

    def __hash__(self) -> int:
        return hash((self.get_name(), self.max_length))

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(str(self.max_length).encode())


@dataclass
class Column(IColumn[T], Generic[T]):
    name: str
    type: IType[T]
    nullable: bool
    default: T | None = None

    def __hash__(self) -> int:
        return hash((self.name, self.type, self.nullable, self.default))

    def get_default_value_hash(self) -> bytes:
        if type(self.default) is str:
            return self.default.encode()
        return bytes()

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> IType[T]:
        return self.type

    def get_is_nullable(self) -> bool:
        return self.nullable

    def get_default(self) -> T | None:
        return self.default
