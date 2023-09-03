from typing import AbstractSet, Any

from .icolumn import IColumn
from .idatabase import IDatabase
from .ihasher import IHasher
from .isql_struct import ISqlStruct, PType
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
    renamed_tables_map = get_renamed_structures(
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


def get_renamed_structures(
    removed: AbstractSet[ISqlStruct],
    added: AbstractSet[ISqlStruct],
    hasher: IHasher,
) -> dict[str, str]:
    added_map = {t.get_params_hash(hasher): t for t in added}
    renamed_map: dict[str, str] = {}
    for t in removed:
        p_hash = t.get_params_hash(hasher)
        if t2 := added_map.pop(p_hash, None):
            renamed_map[t.get_name()] = t2.get_name()
    return renamed_map


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
    t1_columns: list[IColumn[PType]],
    t2_columns: list[IColumn[PType]],
    hasher: IHasher,
) -> dict[str, Any]:
    t1_columns_set = set(t1_columns)
    t2_columns_set = set(t2_columns)
    removed_columns = t1_columns_set - t2_columns_set
    added_columns = t2_columns_set - t1_columns_set
    renamed_columns_map = get_renamed_structures(
        removed_columns, added_columns, hasher
    )
    removed_columns = set(
        filter(
            lambda v: v.get_name() not in renamed_columns_map, removed_columns
        )
    )
    added_columns = set(
        filter(
            lambda v: v.get_name() not in renamed_columns_map.values(),
            added_columns,
        )
    )
    changed_columns: dict[str, Any] = get_changed_columns(
        removed_columns, added_columns, hasher
    )
    removed_columns = set(
        filter(lambda v: v.get_name() not in changed_columns, removed_columns)
    )
    added_columns = set(
        filter(
            lambda v: v.get_name() not in changed_columns,
            added_columns,
        )
    )
    columns_diff: dict[str, Any] = {}
    if len(renamed_columns_map) > 0:
        columns_diff["renamed"] = renamed_columns_map
    if len(removed_columns) > 0:
        columns_diff["removed"] = list(removed_columns)
    if len(added_columns) > 0:
        columns_diff["added"] = list(added_columns)
    if len(changed_columns) > 0:
        columns_diff["changed"] = changed_columns
    return columns_diff


def get_changed_columns(
    removed: set[IColumn[PType]], added: set[IColumn[PType]], hasher: IHasher
) -> dict[str, Any]:
    added_map = {c.get_name(): c for c in added}
    changed_map: dict[str, Any] = {}
    for c in removed:
        name = c.get_name()
        if c2 := added_map.get(name, None):
            changes: dict[str, Any] = {}
            if c.get_type().get_params_hash(
                hasher
            ) != c2.get_type().get_params_hash(hasher):
                changes["type"] = {"from": c.get_type(), "to": c2.get_type()}
            if c.get_is_nullable() != c2.get_is_nullable():
                changes["nullable"] = {
                    "from": c.get_is_nullable(),
                    "to": c2.get_is_nullable(),
                }
            if c.get_default_value_hash() != c2.get_default_value_hash():
                changes["default"] = {
                    "from": c.get_default(),
                    "to": c2.get_default(),
                }
            changed_map[name] = changes
    return changed_map
