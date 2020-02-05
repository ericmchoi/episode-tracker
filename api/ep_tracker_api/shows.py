from flask import Blueprint, request, jsonify, make_response
from ep_tracker_api.auth import key_required
from ep_tracker_api.db import get_db
from werkzeug.exceptions import abort


bp = Blueprint('shows', __name__)


def get_show_from_db(id):
    db = get_db()

    show = db.execute(
        'SELECT * FROM show WHERE id = ?', (id,)
    ).fetchone()

    if show is None:
        abort(make_response(
            jsonify({
                'code': 404,
                'message': 'Show not found.'
            }), 404))

    return show


def get_show_from_response():
    if not request.is_json:
        abort(make_response(
            jsonify({'code': 415, 'message': 'Mimetype is not json.'}), 400))

    show = request.get_json(silent=True)

    if show.keys() < {"title", "totalEpisodes", "lastEpisode", "link"}:
        abort(make_response(
            jsonify({
                'code': 400,
                'message': 'Required parameters missing.'
            }), 400))

    return show


@bp.route('/shows')
@key_required
def index():
    db = get_db()
    shows = db.execute(
        'SELECT id, title, totalEpisodes, lastEpisode, link'
        ' FROM show ORDER BY id ASC'
    ).fetchall()

    return jsonify(shows)


@bp.route('/shows', methods=('POST',))
@key_required
def add_show():
    show = get_show_from_response()

    db = get_db()
    db.execute(
        'INSERT INTO show (title, totalEpisodes, lastEpisode, link)'
        ' VALUES (?, ?, ?, ?)',
        (show['title'], show['totalEpisodes'],
         show['lastEpisode'], show['link'])
    )
    db.commit()

    # TODO: Return location header and/or show id?
    response = make_response('', 200)
    response.mimetype = 'application/json'

    return response


@bp.route('/shows/<int:id>', methods=('DELETE',))
@key_required
def delete_show(id):
    get_show_from_db(id)

    db = get_db()
    db.execute(
        'DELETE FROM show WHERE id = ?', (id,)
    )
    db.commit()

    response = make_response('', 204)
    response.mimetype = 'application/json'

    return response


@bp.route('/shows/<int:id>', methods=('PUT',))
@key_required
def update_show(id):
    get_show_from_db(id)
    show = get_show_from_response()

    db = get_db()
    db.execute(
        'UPDATE show'
        ' SET title = ?, totalEpisodes = ?, lastEpisode = ?, link = ?'
        ' WHERE id = ?',
        (show['title'], show['totalEpisodes'], show['lastEpisode'],
         show['link'], id)
    )
    db.commit()

    response = make_response('', 204)
    response.mimetype = 'application/json'

    return response
