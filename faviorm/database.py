from .idatabase import IDatabase
from .itable import ITable


class Database(IDatabase):
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __hash__(self) -> int:
        return hash((self.name, *self.get_tables()))

    def get_name(self) -> str:
        return self.name

    def get_tables(self) -> list[ITable]:
        tables = []
        for key in dir(self):
            v = getattr(self, key)
            if isinstance(v, ITable):
                tables.append(v)
        return tables
