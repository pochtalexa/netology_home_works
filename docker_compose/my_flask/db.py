import pandas as pd
from sqlalchemy import select
import os


def fill_table(session, table_class, file_name):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(cur_dir, file_name), encoding='utf8', delimiter=';')
    rows = df.to_dict(orient="records")

    temp_advts = session.execute(select(table_class).where(table_class.title == rows[0]['title'])).fetchone()

    if temp_advts is None:
        session.bulk_insert_mappings(table_class, rows)
        session.commit()
        return True

    return False


advts = {
    'items': [
        {
            'title': 'продаю машину',
            'description': 'продаю автомобиль ВАЗ 21213 в отличном состоянии',
            'created_at': '01.07.2021',
            'created_by': 'a.petrov'
        },
        {
            'title': 'продаю мотороллер',
            'description': 'продаю мотороллер Карпаты в хорошем состоянии',
            'created_at': '10.07.2021',
            'created_by': 'i.ivanov'
        },
        {
            'title': 'куплю старые книги',
            'description': 'куплю старые книги в хорошем состоянии',
            'created_at': '05.07.2021',
            'created_by': 'l.dorina'
        }
    ]
}