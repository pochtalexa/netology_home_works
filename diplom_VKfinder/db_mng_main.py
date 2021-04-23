import sqlalchemy
import json

# -------------------------------------------------------------------------------------------------

with open("db_credentials.json") as f:
    db_credentials = json.load(f)

db = f"postgresql://{db_credentials['username']}:{db_credentials['password']}@localhost:5432/{db_credentials['db_name']}"
engine = sqlalchemy.create_engine(db, echo=False)


# -------------------------------------------------------------------------------------------------


class TestDBClearTables:

    def test_clear_users_search(self):
        clear_table = "truncate table users_search;"
        connection = engine.connect()
        sql_res = connection.execute(clear_table)
        sql_res = connection.execute('SELECT count(*) FROM users_search').scalar()
        assert sql_res == 0

    def test_clear_search_results(self):
        clear_table = "truncate table search_results;"
        connection = engine.connect()
        sql_res = connection.execute(clear_table)
        sql_res = connection.execute('SELECT count(*) FROM search_results').scalar()
        assert sql_res == 0


class TestDBCreateTables:

    def test_create_users_search(self):
        create_table = """
            create table if not exists users_search (
            id       serial primary key,
            user_id  integer,
            age      integer,
            sex      integer,
            city_id  integer,
            status   integer,
            "offset" integer);
        """
        connection = engine.connect()
        sql_res = connection.execute(create_table)
        sql_res = connection.execute('SELECT * FROM users_search')
        connection.close()
        assert list(sql_res.keys())[1] == 'user_id'

    def test_create_search_results(self):
        create_table = """
            create table if not exists search_results (
            id      serial primary key,
            user_id integer,
            link    varchar(255),
            url     varchar(255));
        """
        connection = engine.connect()
        sql_res = connection.execute(create_table)
        sql_res = connection.execute('SELECT * FROM search_results')
        connection.close()
        assert list(sql_res.keys())[1] == 'user_id'


class TestDBDropTables:

    def test_drop_users_search(self):
        drop_table = "drop table if exists users_search;"
        connection = engine.connect()
        sql_res = connection.execute(drop_table)
        try:
            sql_res = connection.execute('SELECT * FROM users_search')
        except Exception as e:
            err = e
            connection.close()
        assert str(err).find('users_search') != -1

    def test_drop_search_results(self):
        drop_table = "drop table if exists search_results;"
        connection = engine.connect()
        sql_res = connection.execute(drop_table)
        try:
            sql_res = connection.execute('SELECT * FROM search_results')
        except Exception as e:
            err = e
            connection.close()
        assert str(err).find('search_results') != -1
