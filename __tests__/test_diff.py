import enum

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
        name = faviorm.Column("name", faviorm.VARCHAR(255), True)

    class Users2Table(faviorm.Table):
        id = faviorm.Column("id", faviorm.UUID(), True)

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
        name = faviorm.Column("name", faviorm.VARCHAR(255), True)

    class Users2Table(faviorm.Table):
        id = faviorm.Column("id", faviorm.VARCHAR(255), True)

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
        id = faviorm.Column("id", faviorm.VARCHAR(255), True)

    class Users2Table(faviorm.Table):
        id = faviorm.Column("id", faviorm.UUID(), True)

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


def test_diff_change_nullable_value_of_column() -> None:
    class UsersTable(faviorm.Table):
        id = faviorm.Column("id", faviorm.UUID(), True)

    class Users2Table(faviorm.Table):
        id = faviorm.Column("id", faviorm.UUID(), False)

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
                                "nullable": {
                                    "from": UsersTable.id.get_is_nullable(),
                                    "to": Users2Table.id.get_is_nullable(),
                                }
                            }
                        }
                    }
                }
            }
        }
    }, diff


def test_diff_set_default_value_of_column() -> None:
    class UsersTable(faviorm.Table):
        id = faviorm.Column("id", faviorm.VARCHAR(2), True)

    class Users2Table(faviorm.Table):
        id = faviorm.Column("id", faviorm.VARCHAR(2), True, "default")

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
                                "default": {
                                    "from": UsersTable.id.get_default(),
                                    "to": Users2Table.id.get_default(),
                                }
                            }
                        }
                    }
                }
            }
        }
    }, diff


def test_diff_delete_default_value_of_column() -> None:
    class UsersTable(faviorm.Table):
        id = faviorm.Column("id", faviorm.VARCHAR(2), True, "default")

    class Users2Table(faviorm.Table):
        id = faviorm.Column("id", faviorm.VARCHAR(2), True)

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
                                "default": {
                                    "from": UsersTable.id.get_default(),
                                    "to": Users2Table.id.get_default(),
                                }
                            }
                        }
                    }
                }
            }
        }
    }, diff


def test_diff_change_default_value_of_column() -> None:
    class UsersTable(faviorm.Table):
        id = faviorm.Column("id", faviorm.VARCHAR(2), True, "default")

    class Users2Table(faviorm.Table):
        id = faviorm.Column("id", faviorm.VARCHAR(2), True, "another_default")

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
                                "default": {
                                    "from": UsersTable.id.get_default(),
                                    "to": Users2Table.id.get_default(),
                                }
                            }
                        }
                    }
                }
            }
        }
    }, diff


def test_diff_another_change_type_of_column() -> None:
    class UsersTable(faviorm.Table):
        goods = faviorm.Column(
            "goods", faviorm.ARRAY(faviorm.VARCHAR(255)), True
        )

    class Users2Table(faviorm.Table):
        goods = faviorm.Column("goods", faviorm.JSONB(), True)

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
                            "goods": {
                                "type": {
                                    "from": UsersTable.goods.get_type(),
                                    "to": Users2Table.goods.get_type(),
                                }
                            }
                        }
                    }
                }
            }
        }
    }, diff


def test_diff_change_enum_type_of_column() -> None:
    class ContentType(enum.Enum):
        TRUE_CRIME = "TRUE_CRIME"
        NEWS = "NEWS"
        SPORTS = "SPORTS"

    class BeerType(enum.Enum):
        STOUT = "STOUT"
        GOSE = "GOSE"

    class UsersTable(faviorm.Table):
        types = faviorm.Column("types", faviorm.ENUM(ContentType), True)

    class Users2Table(faviorm.Table):
        types = faviorm.Column("types", faviorm.ENUM(BeerType), True)

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
                            "types": {
                                "type": {
                                    "from": UsersTable.types.get_type(),
                                    "to": Users2Table.types.get_type(),
                                }
                            }
                        }
                    }
                }
            }
        }
    }, diff


def test_change_timestamp_default_value_of_column() -> None:
    class UsersTable(faviorm.Table):
        exp_at = faviorm.Column("exp_at", faviorm.TIMESTAMP(), True, "now")

    class Users2Table(faviorm.Table):
        exp_at = faviorm.Column("exp_at", faviorm.TIMESTAMP(), True, "today")

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
                            "exp_at": {
                                "default": {
                                    "from": UsersTable.exp_at.get_default(),
                                    "to": Users2Table.exp_at.get_default(),
                                }
                            }
                        }
                    }
                }
            }
        }
    }, diff


def test_numeric_column() -> None:
    class UsersTable(faviorm.Table):
        col = faviorm.Column("col", faviorm.NUMERIC(2), False, 222)

    class Users2Table(faviorm.Table):
        col = faviorm.Column("col", faviorm.REAL(), False)

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
                            "col": {
                                "type": {
                                    "from": UsersTable.col.get_type(),
                                    "to": Users2Table.col.get_type(),
                                }
                            }
                        }
                    }
                }
            }
        }
    }, diff


def test_float_column() -> None:
    class UsersTable(faviorm.Table):
        num_col = faviorm.Column(
            "num_col",
            faviorm.FLOAT(2),
            False,
        )

    class Users2Table(faviorm.Table):
        num_col = faviorm.Column("num_col", faviorm.DOUBLE_PRECISION(), False)

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
                            "num_col": {
                                "type": {
                                    "from": UsersTable.num_col.get_type(),
                                    "to": Users2Table.num_col.get_type(),
                                }
                            }
                        }
                    }
                }
            }
        }
    }, diff


def test_column_money_default() -> None:
    class UsersTable(faviorm.Table):
        salary = faviorm.Column("salary", faviorm.MONEY(2), False, "$1000")

    class Users2Table(faviorm.Table):
        salary = faviorm.Column("salary", faviorm.MONEY(2), False, "$2000")

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
                            "salary": {
                                "default": {
                                    "from": UsersTable.salary.get_default(),
                                    "to": Users2Table.salary.get_default(),
                                }
                            }
                        }
                    }
                }
            }
        }
    }, diff


def test_time_and_interal_column() -> None:
    class UsersTable(faviorm.Table):
        time = faviorm.Column(
            "time",
            faviorm.TIME(2),
            False,
        )

    class Users2Table(faviorm.Table):
        time = faviorm.Column("time", faviorm.INTERVAL(2), False)

    class D1(faviorm.Database):
        users = UsersTable("users")

    class D2(faviorm.Database):
        users = Users2Table("users")

    d1 = D1()
    d2 = D2()
    diff = faviorm.diff(d1, d2, hasher=hasher)
    print(diff)
    assert diff == {
        "tables": {
            "changed": {
                "users": {
                    "columns": {
                        "changed": {
                            "time": {
                                "type": {
                                    "from": UsersTable.time.get_type(),
                                    "to": Users2Table.time.get_type(),
                                }
                            }
                        }
                    }
                }
            }
        }
    }, diff
