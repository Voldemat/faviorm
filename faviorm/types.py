import datetime
import decimal
import enum
import uuid
from dataclasses import dataclass
from typing import Any, Literal, Type, TypeVar

from .ihasher import IHasher
from .itype import IType


LTimeMark = Literal["NOW()", "TODAY()"]
LArray = Literal["[]"]
TEnum = TypeVar("TEnum", bound=enum.Enum)


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


class INTEGER(IType[int]):
    def get_name(self) -> Literal["INTEGER"]:
        return "INTEGER"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


class DECIMAL(IType[decimal.Decimal]):
    def get_name(self) -> Literal["DECIMAL"]:
        return "DECIMAL"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


class JSONB(IType[dict[str, Any]]):
    def get_name(self) -> Literal["JSONB"]:
        return "JSONB"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


class BOOLEAN(IType[bool]):
    def get_name(self) -> Literal["BOOLEAN"]:
        return "BOOLEAN"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


class TIMESTAMP(IType[datetime.datetime | LTimeMark]):
    def get_name(self) -> Literal["TIMESTAMP"]:
        return "TIMESTAMP"

    def __hash__(self) -> int:
        return hash((self.get_name()))

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


TArray = TypeVar("TArray", bound=VARCHAR | INTEGER | UUID | BOOLEAN)


@dataclass
class ARRAY(IType[TArray | LArray]):
    def __init__(self, ar_type: TArray) -> None:
        self.ar_type = ar_type

    def get_name(self) -> Literal["ARRAY"]:
        return "ARRAY"

    def __hash__(self) -> int:
        return hash((self.get_name()))

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(str(self.ar_type).encode())


@dataclass
class ENUM(IType[TEnum]):
    def __init__(self, enum: Type[TEnum]) -> None:
        self.enum = enum

    def get_name(self) -> Literal["ENUM"]:
        return "ENUM"

    def __hash__(self) -> int:
        return hash((self.get_name(), self.enum))

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(str(self.enum).encode())
