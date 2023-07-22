from unittest import mock

import pytest

import faviorm


@pytest.mark.parametrize("name", ["main", "test", "check"])
def test_itable(name: str) -> None:
    id_column = mock.MagicMock()
    id_column.get_sql_hash = mock.MagicMock(return_value=b"id_column")
    name_column = mock.MagicMock()
    name_column.get_sql_hash = mock.MagicMock(return_value=b"name_column")

    class MainTable(faviorm.ITable):
        def __hash__(self) -> int:
            return hash((name, id_column, name_column))

        def get_name(self) -> str:
            return name

        def get_columns(self) -> list[faviorm.IColumn]:
            return [id_column, name_column]

    table = MainTable()
    hasher = mock.MagicMock()
    hasher.hash = mock.MagicMock(return_value=b"1")
    assert table.get_sql_hash(hasher) == b"1"
    assert hasher.hash.call_count == 2
    call_args = hasher.hash.call_args_list
    assert call_args[0].args == ([b"id_column", b"name_column"],)
    assert call_args[1].args == ([name.encode(), b"1"],)
