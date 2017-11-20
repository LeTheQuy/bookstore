import os
from flask import Flask, jsonify, g
from flask_sqlalchemy import SQLAlchemy

from order.app.auth import auth
from order.app.decorators import rate_limit
from order.app.decorators.caching import no_cache
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

    @app.after_request
    def after_request(rv):
        headers = getattr(g, 'headers', {})
        rv.headers.extend(headers)
        return rv


    # authentication token route

    @app.route('/get-auth-token')
    @auth.login_required
    @rate_limit(1, 600)
    @no_cache
    @json
    def get_auth_token():
        return {'token': g.user.generate_auth_token()}

    return app
