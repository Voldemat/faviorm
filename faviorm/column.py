from dataclasses import dataclass

from .icolumn import IColumn
from .ihasher import IHasher
from .itype import IType


class UUID(IType):
    def __hash__(self) -> int:
        return hash("UUID")

    def get_sql_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(b"UUID")


@dataclass
class VARCHAR(IType):
    max_length: int

    def __hash__(self) -> int:
        return hash(("VARCHAR", self.max_length))

    def get_sql_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(f"VARCHAR{self.max_length}".encode())


@dataclass
class Column(IColumn):
    name: str
    type: IType

    def __hash__(self) -> int:
        return hash((self.name, self.type))

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> IType:
        return self.type
