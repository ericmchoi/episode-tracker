import os

from flask import Flask, jsonify
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        API_KEY='test',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        ALLOW_CORS=None,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if app.config['ALLOW_CORS']:
        CORS(app, origins=app.config['ALLOW_CORS'])

    from . import db
    db.init_app(app)

    from . import auth

    @app.route('/')
    @auth.key_required
    def index():
        return jsonify({'status': 'up'})

    from . import shows
    app.register_blueprint(shows.bp)

    return app
