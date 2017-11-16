import os
from flask import Flask, jsonify, g
from flask_sqlalchemy import SQLAlchemy

from order.app.auth import auth
from order.app.decorators.json import json

db = SQLAlchemy()


def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # apply configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # initialize extensions
    db.init_app(app)

    # register blueprints
    from .api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    # authentication token route

    @app.route('/get-auth-token')
    @auth.login_required
    @json
    def get_auth_token():
        return {'token': g.user.generate_auth_token()}

    return app
