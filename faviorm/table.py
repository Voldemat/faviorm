from .icolumn import IColumn
from .itable import ITable


class Table(ITable):
    table_name: str

    def __init__(self, name: str) -> None:
        self.table_name = name

    def __hash__(self) -> int:
        return hash((self.table_name, *self.get_columns()))

    def get_name(self) -> str:
        return self.table_name

    def get_columns(self) -> list[IColumn]:
        columns = []
        for key in dir(self):
            v = getattr(self, key)
            if isinstance(v, IColumn):
                columns.append(v)
        return columns
