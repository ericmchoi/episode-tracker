import functools

from flask import current_app, request, make_response, jsonify
from werkzeug.exceptions import abort


def key_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        auth_header = request.headers.get('Authorization')
        values = auth_header.split(' ') if auth_header else []
        key = values[1] if len(values) == 2 else ''

        if key != current_app.config['API_KEY']:
            abort(make_response(
                jsonify({'code': 401, 'message': 'Unauthorized'}), 401))

        return view(**kwargs)

    return wrapped_view
