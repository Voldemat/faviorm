from .idatabase import IDatabase
from .itable import ITable


class Database(IDatabase):
    name: str
    tables: list[ITable]

    def __init__(self, name: str) -> None:
        self.name = name

    def get_tables(self) -> list[ITable]:
        tables = []
        for key in dir(self):
            v = getattr(self, key)
            if isinstance(v, ITable):
                tables.append(v)
        return tables
