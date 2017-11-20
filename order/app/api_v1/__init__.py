from flask import Blueprint

from order.app.auth import auth_token
from order.app.api_v1 import custommers, products, orders, items, errors
from order.app.decorators import rate_limit
from order.app.decorators.caching import etag

api = Blueprint('api', __name__)


@api.before_request
@rate_limit(limit=5, period=15)
@auth_token.login_required
def before_request():
    pass


@api.after_request
@etag
def after_request(rv):
   return rv

