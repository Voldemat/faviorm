from typing import Generic
from unittest import mock

import pytest

import faviorm
from faviorm import T


@pytest.mark.parametrize("name", ["main", "test", "check"])
def test_icolumn(name: str) -> None:
    t_type = mock.MagicMock()
    t_type.get_sql_hash = mock.MagicMock(return_value=b"t_type")

    class TestColumn(faviorm.IColumn[T], Generic[T]):
        def __hash__(self) -> int:
            return hash((name, t_type))

        def get_name(self) -> str:
            return name

        def get_type(self) -> faviorm.IType[T]:
            return t_type

        def get_is_nullable(self) -> bool:
            return True

        def get_default(self) -> T | None:
            return t_type

        def get_default_value_hash(self) -> bytes:
            return bytes()

    column = TestColumn[str]()
    hasher = mock.MagicMock()
    hasher.hash = mock.MagicMock(return_value=b"1")
    assert column.get_sql_hash(hasher) == b"1"
    assert hasher.hash.call_count == 2
    assert hasher.hash.call_args.args == ([name.encode(), b"1"],)
