from typing import Any
from unittest import mock

from faviorm import IColumn, IDatabase, IType, SQLLoader, VARCHAR
from faviorm.loader import QUERIES


async def get_result(query: str, *args: Any, **kwargs: Any) -> list[Any]:
    if query == QUERIES["tables"]:
        return [["apples"], ["oranges"]]
    elif query == QUERIES["columns"]:
        return [
            ["apples", "name", "character varying", "NO"],
        ]

    return []


async def test_loader() -> None:
    executor_mock = mock.MagicMock()
    executor_mock.execute = mock.AsyncMock(wraps=get_result)
    loader = SQLLoader(executor_mock)

    db = await loader.load()

    assert isinstance(db, IDatabase)
    tables = db.get_tables()
    assert len(tables) == 2
    apples_table = tables[0]
    oranges_table = tables[1]
    assert apples_table.get_name() == "apples"
    assert oranges_table.get_name() == "oranges"
    apples_columns: list[IColumn[IType[Any]]] = apples_table.get_columns()
    assert len(apples_columns) == 1
    apples_name_column = apples_columns[0]
    assert apples_name_column.get_name() == "name"
    assert apples_name_column.get_type() == VARCHAR(255)
    assert apples_name_column.get_is_nullable() is False

    assert len(oranges_table.get_columns()) == 0
