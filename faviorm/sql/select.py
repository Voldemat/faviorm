from ..icolumn import IColumn
from ..isql_struct import PType


def select(*args: IColumn[PType]) -> tuple[PType]:
    return args  # type: ignore
