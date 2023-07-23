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
        return list(
            filter(
                lambda v: isinstance(v, ITable),
                map(
                    lambda key: getattr(self, key),
                    dir(self),
                ),
            )
        )
