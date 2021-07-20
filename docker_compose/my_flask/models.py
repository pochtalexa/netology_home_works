import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import os


cur_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cur_dir, 'db_credentials.json')) as f:
    db_credentials = json.load(f)

DSN = f"postgresql://{db_credentials['username']}:{db_credentials['password']}@db_container:5432/flask_orm"

engine = sq.create_engine(DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# connection = engine.connect()


class Advts(Base):
    __tablename__ = 'advertisements'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(30))
    description = sq.Column(sq.String(256))
    created_at = sq.Column(sq.Date)
    created_by = sq.Column(sq.String(30))

    def __str__(self):
        result = (f'id={self.id}\ttitle={self.title}\tdescription={self.description}\t'
                  f'created_at={self.created_at}\tcreated_by={self.created_by}')
        return result

    def __repr__(self):
        return str(self)


def create_tables():
    Base.metadata.create_all(bind=engine)
