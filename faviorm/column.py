from dataclasses import dataclass

from .ihasher import IHasher
from .isql_struct import ISqlStruct


class UUID(ISqlStruct):
    def __hash__(self) -> int:
        return hash("UUID")

    def get_sql_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(b"UUID")


@dataclass
class VARCHAR(ISqlStruct):
    max_length: int

    def __hash__(self) -> int:
        return hash(("VARCHAR", self.max_length))

    def get_sql_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(f"VARCHAR{self.max_length}".encode())


COLUMN_TYPE = UUID | VARCHAR


@dataclass
class Column(ISqlStruct):
    name: str
    type: COLUMN_TYPE

    def __hash__(self) -> int:
        return hash((self.name, self.type))

    def get_sql_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(
            [self.name.encode(), self.type.get_sql_hash(hasher)]
        )
