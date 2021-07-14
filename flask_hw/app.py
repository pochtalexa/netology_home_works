from flask import Flask, jsonify, request, make_response
from db import advts
import validators
from validators import validate

app = Flask(__name__)


@app.route('/api/v1/<int:advt_id>', methods=['GET'], )
def advt_list(advt_id):
    if advt_id < 0 or advt_id > len(advts['items']) - 1:
        resp = make_response(jsonify({'status': False, 'description': 'advertisement id is out of range'}), 404)
        return resp
    return jsonify(advts['items'][advt_id])


@app.route('/api/v1', methods=['GET'], )
def advt_list_all():
    return jsonify(advts['items'])


@app.route('/api/v1', methods=['POST'], )
@validate(validators.POST)
def advt_add():
    item = request.get_json()
    advts['items'].append(item)
    return jsonify({'message': 'advertisement added'})


@app.route('/api/v1/<int:advt_id>', methods=['DELETE'], )
def advt_del(advt_id):
    if advt_id < 0 or advt_id > len(advts['items']) - 1:
        resp = make_response(jsonify({'status': False, 'description': 'advertisement id is out of range'}), 404)
        return resp
    del advts['items'][advt_id]
    return jsonify({'message': f'advertisement with id {advt_id} deleted'})


if __name__ == '__main__':
    app.run(port=5051, debug=True)
