from flask import Blueprint

from order.app.auth import auth_token
from order.app.api_v1 import custommers, products, orders, items, errors

api = Blueprint('api', __name__)


@api.before_request
@auth_token.login_required
def before_request():
    pass


