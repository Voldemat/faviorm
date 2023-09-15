from typing import Iterable

from .idatabase import IDatabase
from .itable import ITable


class Database(IDatabase):
    def __init__(self, tables: Iterable[ITable] = []) -> None:
        for table in tables:
            setattr(self, table.get_name(), table)

    def __hash__(self) -> int:
        return hash(self.get_tables())

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
