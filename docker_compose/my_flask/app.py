import os
from flask import Flask, jsonify, request, make_response
# from db import advts
import validators
from validators import validate
from db import fill_table
from models import Advts, create_tables, Session
import psycopg2
from sqlalchemy import insert


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        if column.name == 'id':
            continue
        d[column.name] = str(getattr(row, column.name))

    return d


app = Flask(__name__)


@app.route('/api/v1/<int:advt_id>', methods=['GET'], )
def advt_list(advt_id):
    advts = session.query(Advts).all()

    if advt_id < 0 or advt_id > len(advts) - 1:
        resp = make_response(jsonify({'status': False, 'description': 'advertisement id is out of range'}), 404)
        return resp

    advt = row2dict(advts[advt_id])

    return jsonify(advt)


@app.route('/api/v1', methods=['GET'], )
def advt_list_all():
    result = []

    advts = session.query(Advts).all()

    for advt in advts:
        result.append(row2dict(advt))

    return jsonify(result)


@app.route('/api/v1', methods=['POST'], )
@validate(validators.POST)
def advt_add():
    item = request.get_json()

    session.execute(insert(Advts).values(**item))
    session.commit()

    return jsonify({'message': 'advertisement added'})


@app.route('/api/v1/<int:advt_id>', methods=['DELETE'], )
def advt_del(advt_id):
    advts = session.query(Advts).all()

    if advt_id < 0 or advt_id > len(advts) - 1:
        resp = make_response(jsonify({'status': False, 'description': 'advertisement id is out of range'}), 404)
        return resp

    id = advts[advt_id].id

    session.query(Advts).filter(Advts.id == id).delete()
    session.commit()

    return jsonify({'message': f'advertisement with id {advt_id} deleted'})


if __name__ == '__main__':
    create_tables()

    session = Session()

    fill_table(session, Advts, 'advts.csv')

    port = int(os.environ.get('MYTESTPORT', 5050))
    app.run(host='0.0.0.0', port=port, debug=True)
