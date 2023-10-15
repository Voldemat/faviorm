import datetime
import decimal
import enum
import uuid
from dataclasses import dataclass
from typing import Literal, Type, TypeVar

from .ihasher import IHasher
from .itype import IType

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


class BOOLEAN(IType[bool]):
    def get_name(self) -> Literal["BOOLEAN"]:
        return "BOOLEAN"

    def __hash__(self) -> int:
        return hash(self.get_name())

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

    def __getitem__(self, index: int) -> int:
        return self[index]

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


@dataclass
class NUMERIC(IType[int | decimal.Decimal]):
    accuracy: int
    scale: int = 0

    def __post_init__(self) -> None:
        if self.scale < 0:
            raise TypeError()
        elif 1000 < self.accuracy or self.accuracy <= 0:
            raise TypeError()

    def get_name(self) -> Literal["NUMERIC"]:
        return "NUMERIC"

    def __hash__(self) -> int:
        return hash((self.get_name(), self.scale, self.accuracy))

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(str((self.accuracy, self.scale)).encode())


class REAL(IType[float]):
    def get_name(self) -> Literal["REAL"]:
        return "REAL"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


class DOUBLE_PRECISION(IType[float]):
    def get_name(self) -> Literal["DOUBLE_PRECISION"]:
        return "DOUBLE_PRECISION"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


T_FLOAT = TypeVar("T_FLOAT", bound=REAL | DOUBLE_PRECISION)


@dataclass
class FLOAT(IType[float]):
    p: int = 0

    def __post_init__(self) -> None:
        if 1 > self.p or self.p > 53:
            raise TypeError()

    def get_name(self) -> Literal["FLOAT"]:
        return "FLOAT"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(str((self.p)).encode())


@dataclass
class MONEY(IType[str | int | decimal.Decimal | float]):
    lc_monetary: int = 0

    def get_name(self) -> Literal["MONEY"]:
        return "MONEY"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(str(self.lc_monetary).encode())


class SMALLINT(IType[int]):
    def get_name(self) -> Literal["SMALLINT"]:
        return "SMALLINT"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


class BIGINT(IType[int]):
    def get_name(self) -> Literal["BIGINT"]:
        return "BIGINT"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


class BYTEA(IType[bytes]):
    def get_name(self) -> Literal["BYTEA"]:
        return "BYTEA"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


DATETIME_VALUES = Literal[
    "epoch", "infinity", "-infinity", "today", "tomorrow", "yesterday", "now"
]
TIME_VALUES = Literal["now", "allballs"]


class TIMESTAMP(IType[datetime.datetime | DATETIME_VALUES]):
    def get_name(self) -> Literal["TIMESTAMP"]:
        return "TIMESTAMP"

    def __hash__(self) -> int:
        return hash((self.get_name()))

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


@dataclass
class TIMESTAMPTZ(IType[datetime.datetime | DATETIME_VALUES]):
    p: int = 0

    def get_name(self) -> Literal["TIMESTAMPTZ"]:
        return "TIMESTAMPTZ"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(str((self.p)).encode())


class DATE(IType[datetime.date | DATETIME_VALUES]):
    def get_name(self) -> Literal["DATE"]:
        return "DATE"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


@dataclass
class TIME(IType[datetime.time | TIME_VALUES]):
    p: int = 0

    def get_name(self) -> Literal["TIME"]:
        return "TIME"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(str((self.p)).encode())


@dataclass
class TIMETZ(IType[datetime.time | TIME_VALUES]):
    p: int = 0

    def get_name(self) -> Literal["TIMETZ"]:
        return "TIMETZ"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(str((self.p)).encode())


INTERVAL_VALUES = Literal[
    "YEAR",
    "MONTH",
    "DAY",
    "HOUR",
    "MINUTE",
    "SECOND",
    "YEAR TO MONTH",
    "DAY TO HOUR",
    "DAY TO MINUTE",
    "DAY TO SECOND",
    "HOUR TO MINUTE",
    "HOUR TO SECOND",
    "MINUTE TO SECOND",
]


@dataclass
class INTERVAL(IType[datetime.time]):
    p: int = 0
    values: INTERVAL_VALUES | None = None

    def get_name(self) -> Literal["INTERVAL"]:
        return "INTERVAL"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(str((self.p, self.values)).encode())


class TSVECTOR(IType[str]):
    def get_name(self) -> Literal["TSVECTOR"]:
        return "TSVECTOR"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


TJSON = TypeVar("TJSON", bound=str | int | bool | None)


class JSON(IType[dict[str | int | bool | None, str | int | bool | None]]):
    def get_name(self) -> Literal["JSON"]:
        return "JSON"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def __getitem__(self, key: TJSON) -> TJSON:
        return self[key]

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""


class JSONB(IType[bytes]):
    def get_name(self) -> Literal["JSONB"]:
        return "JSONB"

    def __hash__(self) -> int:
        return hash(self.get_name())

    def get_params_hash(self, hasher: IHasher) -> bytes:
        return b""
