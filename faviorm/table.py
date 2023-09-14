from typing import Any, Iterable

from .icolumn import IColumn
from .isql_struct import PType
from .itable import ITable
from .itype import IType


class Table(ITable):
    table_name: str

    def __init__(
        self, name: str, columns: Iterable[IColumn[IType[Any]]] = []
    ) -> None:
        self.table_name = name
        for column in columns:
            setattr(self, column.get_name(), column)

    def __hash__(self) -> int:
        return hash((self.table_name, *self.get_columns()))

    def get_name(self) -> str:
        return self.table_name

    def get_columns(self) -> list[IColumn[PType]]:
        return list(
            filter(
                lambda v: isinstance(v, IColumn),
                map(lambda key: getattr(self, key), dir(self)),
            )
        )
