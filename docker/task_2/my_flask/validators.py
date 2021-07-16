import jsonschema
from flask import request, make_response, jsonify

POST = {
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'created_at': {
            'type': 'string',
            'pattern': '^\d{1,2}\.\d{1,2}\.\d{4}$'
        },
        'created_by': {
            'type': 'string'
        }
    }
}


def validate(req_schema):
    """Валидатор входящих запросов"""

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                jsonschema.validate(
                    request.get_json(), schema=req_schema,
                )
            except jsonschema.ValidationError as er:
                resp = make_response(jsonify({'success': False, 'description': er.message}))
                resp.set_status = 401
                return resp
            result = func(*args, **kwargs)

            return result

        return wrapper

    return decorator
