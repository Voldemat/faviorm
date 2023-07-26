import faviorm

hasher = faviorm.MD5Hasher()


def test_diff_tables_names() -> None:
    class UsersTable(faviorm.Table):
        pass

    class D1(faviorm.Database):
        users = UsersTable("users")

    class D2(faviorm.Database):
        users = UsersTable("files")

    d1 = D1()
    d2 = D2()
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

    d1 = D1()
    d2 = D2()
    diff = faviorm.diff(d1, d2, hasher=hasher)
    assert diff == {}, diff


def test_diff_added_column_and_removed_column() -> None:
    class UsersTable(faviorm.Table):
        name = faviorm.Column("name", faviorm.VARCHAR(255))

    class Users2Table(faviorm.Table):
        id = faviorm.Column("id", faviorm.UUID())

    class D1(faviorm.Database):
        users = UsersTable("users")

    class D2(faviorm.Database):
        users = Users2Table("users")

    d1 = D1()
    d2 = D2()
    diff = faviorm.diff(d1, d2, hasher=hasher)
    assert diff == {
        "tables": {
            "changed": {
                "users": {
                    "columns": {
                        "added": [Users2Table.id],
                        "removed": [UsersTable.name],
                    }
                }
            }
        }
    }, diff


def test_diff_rename_column() -> None:
    class UsersTable(faviorm.Table):
        name = faviorm.Column("name", faviorm.VARCHAR(255))

    class Users2Table(faviorm.Table):
        id = faviorm.Column("id", faviorm.VARCHAR(255))

    class D1(faviorm.Database):
        users = UsersTable("users")

    class D2(faviorm.Database):
        users = Users2Table("users")

    d1 = D1()
    d2 = D2()
    diff = faviorm.diff(d1, d2, hasher=hasher)
    assert diff == {
        "tables": {
            "changed": {"users": {"columns": {"renamed": {"name": "id"}}}}
        }
    }, diff


def test_diff_change_type_of_column() -> None:
    class UsersTable(faviorm.Table):
        id = faviorm.Column("id", faviorm.VARCHAR(255))

    class Users2Table(faviorm.Table):
        id = faviorm.Column("id", faviorm.UUID())

    class D1(faviorm.Database):
        users = UsersTable("users")

    class D2(faviorm.Database):
        users = Users2Table("users")

    d1 = D1()
    d2 = D2()
    diff = faviorm.diff(d1, d2, hasher=hasher)
    assert diff == {
        "tables": {
            "changed": {
                "users": {
                    "columns": {
                        "changed": {
                            "id": {
                                "type": {
                                    "from": UsersTable.id.get_type(),
                                    "to": Users2Table.id.get_type(),
                                }
                            }
                        }
                    }
                }
            }
        }
    }, diff
