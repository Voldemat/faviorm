from .icolumn import IColumn
from .isql_struct import T
from .itable import ITable


class Table(ITable):
    table_name: str

    def __init__(self, name: str) -> None:
        self.table_name = name

    def __hash__(self) -> int:
        return hash((self.table_name, *self.get_columns()))

    def get_name(self) -> str:
        return self.table_name

    def get_columns(self) -> list[IColumn[T]]:
        return list(
            filter(
                lambda v: isinstance(v, IColumn),
                map(lambda key: getattr(self, key), dir(self)),
            )
        )
