from unittest import mock

import pytest

import faviorm


@pytest.mark.parametrize("name", ["main", "test", "check"])
def test_idatabase(name: str) -> None:
    table1 = mock.MagicMock()
    table1.get_sql_hash = mock.MagicMock(return_value=b"table1")
    table2 = mock.MagicMock()
    table2.get_sql_hash = mock.MagicMock(return_value=b"table2")

    class MainDatabase(faviorm.IDatabase):
        def __hash__(self) -> int:
            return hash((name, table1, table2))

        def get_name(self) -> str:
            return name

        def get_tables(self) -> list[faviorm.ITable]:
            return [table1, table2]

    db = MainDatabase()
    hasher = mock.MagicMock()
    hasher.hash = mock.MagicMock(return_value=b"1")
    assert db.get_sql_hash(hasher) == b"1"
    assert hasher.hash.call_count == 2
    call_args = hasher.hash.call_args_list
    assert call_args[0].args == ([b"table1", b"table2"],)
    assert call_args[1].args == ([name.encode(), b"1"],)
