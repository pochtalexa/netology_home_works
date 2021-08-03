from gino import Gino
import json

with open('db_credentials.json', ) as f:
    db_credentials = json.load(f)

PG_DSN = f"postgresql://{db_credentials['username']}:{db_credentials['password']}@localhost:5432/netology_async"

db = Gino()

class People(db.Model):

    __tablename__ = 'people'

    id = db.Column(db.Integer(), primary_key=True)
    birth_year = db.Column(db.String(10))
    eye_color = db.Column(db.String(50))
    films = db.Column(db.Text)
    gender = db.Column(db.String(50))
    hair_color = db.Column(db.String(50))
    height = db.Column(db.String(50))
    homeworld = db.Column(db.String(100))
    mass = db.Column(db.String(50))
    name = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))
    species = db.Column(db.Text)
    starships = db.Column(db.Text)
    vehicles = db.Column(db.Text)

    def __str__(self):
        result = f'id={self.id}\tname={self.name}\tbirth_year={self.birth_year}'
        return result

    def __repr__(self):
        return str(self)

