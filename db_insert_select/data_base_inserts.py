import sqlalchemy
import os
import json


# Const -------------------------------------------------------------------------------------------------
with open('db_credentials.json', ) as f:
    db_credentials = json.load(f)

db = f"postgresql://{db_credentials['username']}:{db_credentials['password']}@localhost:5432/netology_db"

run_order = ['singer', 'collection', 'genre', 'album', 'track', 'singer_genre', 'singer_album', 'collection_track']

# Const -------------------------------------------------------------------------------------------------


# Func -------------------------------------------------------------------------------------------------
def run_inserts(run_order):
    for name in run_order:
        print(name)
        file_name = f'{name}.sql'
        with open(os.path.join('./SQL', file_name), encoding='utf8') as f:
            while True:
                line = f.readline()
                if not line or line == '':
                    break
                else:
                    res = connection.execute(line)
    return True


# Func -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    # print(engine.table_names())

    run_inserts(run_order)

    print('- done')





