from typing import Any

from .idatabase import IDatabase
from .ihasher import IHasher


def diff(d1: IDatabase, d2: IDatabase, hasher: IHasher) -> dict[str, Any]:
    dif: dict[str, Any] = {}
    d1_name = d1.get_name()
    d2_name = d2.get_name()
    if d1_name != d2_name:
        dif["name"] = [d1_name, d2_name]
    d1_tables = set(d1.get_tables())
    d2_tables = set(d2.get_tables())
    removed_tables = d1_tables - d2_tables
    added_tables = d2_tables - d1_tables
    added_tables_map = {t.get_params_hash(hasher): t for t in added_tables}
    removed_tables_map = {t.get_params_hash(hasher): t for t in removed_tables}
    renamed_tables = []
    for t in removed_tables:
        p_hash = t.get_params_hash(hasher)
        if t2 := added_tables_map.pop(p_hash, None):
            del removed_tables_map[p_hash]
            renamed_tables.append({"from": t.get_name(), "to": t2.get_name()})
    tables_dif: dict[str, Any] = {}
    if len(removed_tables_map) > 0:
        tables_dif["removed"] = list(
            map(lambda t: t.get_name(), removed_tables_map.values())
        )
    if len(added_tables_map) > 0:
        tables_dif["added"] = list(
            map(lambda t: t.get_name(), added_tables_map.values())
        )
    if len(renamed_tables) > 0:
        tables_dif["renamed"] = renamed_tables
    if tables_dif != {}:
        dif["tables"] = tables_dif
    return dif
