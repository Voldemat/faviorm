from typing import Any

from .icolumn import IColumn
from .idatabase import IDatabase
from .ihasher import IHasher
from .itable import ITable


def diff(d1: IDatabase, d2: IDatabase, hasher: IHasher) -> dict[str, Any]:
    dif: dict[str, Any] = {}
    d1_name = d1.get_name()
    d2_name = d2.get_name()
    if d1_name != d2_name:
        dif["name"] = [d1_name, d2_name]
    d1_tables = set(d1.get_tables())
    d2_tables = set(d2.get_tables())
    if tables_dif := get_tables_diff(d1_tables, d2_tables, hasher):
        dif["tables"] = tables_dif
    return dif


def get_tables_diff(
    d1_tables: set[ITable], d2_tables: set[ITable], hasher: IHasher
) -> dict[str, Any] | None:
    removed_tables = d1_tables - d2_tables
    added_tables = d2_tables - d1_tables
    renamed_tables_map = get_renamed_tables(
        removed_tables, added_tables, hasher
    )
    removed_tables = set(
        filter(
            lambda t: t.get_name() not in renamed_tables_map, removed_tables
        )
    )
    added_tables = set(
        filter(
            lambda t: t.get_name() not in renamed_tables_map.values(),
            added_tables,
        )
    )
    changed_tables_map = get_changed_tables(
        removed_tables, added_tables, hasher
    )
    removed_tables = set(
        filter(
            lambda t: t.get_name() not in changed_tables_map, removed_tables
        )
    )
    added_tables = set(
        filter(lambda t: t.get_name() not in changed_tables_map, added_tables)
    )
    tables_dif: dict[str, Any] = {}
    if len(removed_tables) > 0:
        tables_dif["removed"] = list(
            map(lambda t: t.get_name(), removed_tables)
        )
    if len(added_tables) > 0:
        tables_dif["added"] = list(map(lambda t: t.get_name(), added_tables))
    if len(renamed_tables_map) > 0:
        tables_dif["renamed"] = renamed_tables_map
    if len(changed_tables_map) > 0:
        tables_dif["changed"] = changed_tables_map
    return tables_dif if tables_dif != {} else None


def get_renamed_tables(
    removed_tables: set[ITable], added_tables: set[ITable], hasher: IHasher
) -> dict[str, str]:
    added_tables_map = {t.get_params_hash(hasher): t for t in added_tables}
    renamed_tables_map: dict[str, str] = {}
    for t in removed_tables:
        p_hash = t.get_params_hash(hasher)
        if t2 := added_tables_map.pop(p_hash, None):
            renamed_tables_map[t.get_name()] = t2.get_name()
    return renamed_tables_map


def get_changed_tables(
    removed_tables: set[ITable], added_tables: set[ITable], hasher: IHasher
) -> dict[str, Any]:
    added_tables_map = {t.get_name(): t for t in added_tables}
    changed_tables_map: dict[str, Any] = {}
    for t in removed_tables:
        name = t.get_name()
        if t2 := added_tables_map.pop(name, None):
            changed_tables_map[name] = {
                "columns": get_columns_diff(
                    t.get_columns(), t2.get_columns(), hasher
                )
            }
    return changed_tables_map


def get_columns_diff(
    t1_columns: list[IColumn], t2_columns: list[IColumn], hasher: IHasher
) -> dict[str, Any]:
    t1_columns_set = set(t1_columns)
    t2_columns_set = set(t2_columns)
    removed_columns = t1_columns_set - t2_columns_set
    added_columns = t2_columns_set - t1_columns_set
    columns_diff = {}
    if len(removed_columns) > 0:
        columns_diff["removed"] = list(removed_columns)
    if len(added_columns) > 0:
        columns_diff["added"] = list(added_columns)
    return columns_diff