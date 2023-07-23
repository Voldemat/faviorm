import faviorm

hasher = faviorm.MD5Hasher()


def test_diff_name() -> None:
    class D(faviorm.Database):
        pass

    d1 = D("d1")
    d2 = D("d2")
    diff = faviorm.diff(d1, d2, hasher=hasher)
    assert diff == {
        "name": ["d1", "d2"],
    }


def test_diff_tables_names() -> None:
    class UsersTable(faviorm.Table):
        pass

    class D1(faviorm.Database):
        users = UsersTable("users")

    class D2(faviorm.Database):
        users = UsersTable("files")

    d1 = D1("same name")
    d2 = D2("same name")
    diff = faviorm.diff(d1, d2, hasher=hasher)
    assert diff == {
        "tables": {
            "renamed": {
                "users": "files",
            }
        }
    }, diff


def test_not_diff_with_different_tables_classes() -> None:
    class UsersTable(faviorm.Table):
        pass

    class Users2Table(faviorm.Table):
        pass

    class D1(faviorm.Database):
        users = UsersTable("users")

    class D2(faviorm.Database):
        users = Users2Table("users")

    d1 = D1("same name")
    d2 = D2("same name")
    diff = faviorm.diff(d1, d2, hasher=hasher)
    assert diff == {}, diff


def test_diff_added_column() -> None:
    class UsersTable(faviorm.Table):
        pass

    class Users2Table(faviorm.Table):
        id = faviorm.Column("id", faviorm.UUID())

    class D1(faviorm.Database):
        users = UsersTable("users")

    class D2(faviorm.Database):
        users = Users2Table("users")

    d1 = D1("same name")
    d2 = D2("same name")
    diff = faviorm.diff(d1, d2, hasher=hasher)
    assert diff == {
        "tables": {
            "changed": {"users": {"columns": {"added": [Users2Table.id]}}}
        }
    }, diff
