import iorm


class UsersTable(iorm.Table):
    id = iorm.Column(name="id", type=iorm.UUID())
    name = iorm.Column(name="name", type=iorm.VARCHAR(255))


class MainDatabase(iorm.Database):
    users = UsersTable("users")


db = MainDatabase("iorm")
h = db.get_sql_hash()
print(h)
