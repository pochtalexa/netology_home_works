import sqlalchemy
import pandas as pd
import json

# Const -------------------------------------------------------------------------------------------------
# отображать все колонки
pd.set_option('display.max_columns', 30)
pd.set_option("max_colwidth", 50)
pd.set_option("display.max_rows", 150)

with open('db_credentials.json', ) as f:
    db_credentials = json.load(f)

db = f"postgresql://{db_credentials['username']}:{db_credentials['password']}@localhost:5432/netology_db"

select_1 = """
select a.title, a.release_year from album as a
where a.release_year = 2018;
"""

select_2 = """
select a.title, a.duration from track as a
order by a.duration desc
limit(1);
"""

select_3 = """
select a.title, a.duration from track as a
where a.duration >= 3.5;
"""

select_4 = """
select a.title from collection as a
where a.release_year between 2018 and 2020;
"""

select_5 = """
select a.first_name, a.middle_name, a.last_name, a.nickname from singer as a
where a.first_name not like '%% %%';
"""

select_6 = """
select a.title from track as a
where a.title like '%%мой%%' or a.title like '%%Мой%%'
   or a.title like '%%my%%' or a.title like '%%My%%';
"""

selects = [select_1, select_2, select_3, select_4, select_5, select_6]


# Const -------------------------------------------------------------------------------------------------


# Func -------------------------------------------------------------------------------------------------
def run_selects(selects, connection):
    for select in selects:
        df = pd.read_sql_query(sql=select, con=connection)
        print(50 * '-')
        print(df)

    print(50 * '-')

    return True


# Func -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    # print(engine.table_names())

    res = run_selects(selects, connection)

    print('- done')
