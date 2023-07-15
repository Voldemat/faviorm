from .column import Column
from .ihasher import IHasher
from .isql_struct import ISqlStruct, map_get_sql_hash


class Table(ISqlStruct):
    table_name: str

    def __init__(self, name: str) -> None:
        self.table_name = name

    def get_columns(self) -> list[Column]:
        columns = []
        for key in dir(self):
            v = getattr(self, key)
            if isinstance(v, Column):
                columns.append(v)
        return columns

    def get_sql_hash(self, hasher: IHasher) -> bytes:
        return hasher.hash(
            [
                self.table_name.encode(),
                *list(map_get_sql_hash(hasher, self.get_columns())),
            ]
        )
