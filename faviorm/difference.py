from typing import Any

from .idatabase import IDatabase


def diff(d1: IDatabase, d2: IDatabase) -> dict[str, Any]:
    dif: dict[str, Any] = {}
    d1_name = d1.get_name()
    d2_name = d2.get_name()
    if d1_name != d2_name:
        dif["name"] = [d1_name, d2_name]
    d1_tables = set(d1.get_tables())
    d2_tables = set(d2.get_tables())
    removed_tables = d1_tables - d2_tables
    added_tables = d2_tables - d1_tables
    if len(removed_tables) > 0 or len(added_tables) > 0:
        dif["tables"] = {
            "added": list(map(lambda t: t.get_name(), added_tables)),
            "removed": list(map(lambda t: t.get_name(), removed_tables)),
        }
    return dif
