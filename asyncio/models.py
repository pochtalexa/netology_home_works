import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

with open('db_credentials.json', ) as f:
    db_credentials = json.load(f)

DSN = f"postgresql://{db_credentials['username']}:{db_credentials['password']}@localhost:5432/netology_async"

engine = sq.create_engine(DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# connection = engine.connect()


class People(Base):
    __tablename__ = 'people'

    id = sq.Column(sq.Integer, primary_key=True)
    birth_year = sq.Column(sq.String(10))
    eye_color = sq.Column(sq.String(50))
    films = sq.Column(sq.Text)
    gender = sq.Column(sq.String(50))
    hair_color = sq.Column(sq.String(50))
    height = sq.Column(sq.String(50))
    homeworld = sq.Column(sq.String(100))
    mass = sq.Column(sq.String(50))
    name = sq.Column(sq.String(50))
    skin_color = sq.Column(sq.String(50))
    species = sq.Column(sq.Text)
    starships = sq.Column(sq.Text)
    vehicles = sq.Column(sq.Text)

    def __str__(self):
        result = f'id={self.id}\tname={self.name}\tbirth_year={self.birth_year}'
        return result

    def __repr__(self):
        return str(self)


def create_tables():
    Base.metadata.create_all(bind=engine)
