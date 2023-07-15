from faviorm import Database


def test_database() -> None:
    class MainDatabase(Database):
        pass

    db = MainDatabase("main")
    assert db.get_sql_hash() is not None
