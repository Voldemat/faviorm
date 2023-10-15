import faviorm
from faviorm.sql.select import select


class UserTable(faviorm.Table):
    name = faviorm.Column("name", faviorm.VARCHAR(255), nullable=False)
    login = faviorm.Column("login", faviorm.types.INTEGER(), nullable=False)


def test_select() -> None:
    query = select(UserTable.name, UserTable.login)
    assert isinstance(query, tuple)
