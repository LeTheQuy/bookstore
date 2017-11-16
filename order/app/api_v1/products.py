from flask import jsonify, request

from order.app import db, json
from order.app.api_v1 import api
from order.app.decorators.paginate import paginate
from order.app.models import Product


@api.route('/products/', methods=['GET'])
@json
@paginate('products')
def get_products():
    return Product.query


@api.route('/products/<int:id>', methods=['GET'])
@json
def get_product(id):
    return Product.query.get_or_404(id).export_data()


@api.route('/products/', methods=['POST'])
@json
def new_product():
    product = Product()
    product.import_data(request.json)
    db.session.add(product)
    db.session.commit()
    return {}, 201, {'Location': product.get_url()}


@api.route('/products/<int:id>', methods=['PUT'])
@json
def edit_product(id):
    product = Product.query.get_or_404(id)
    product.import_data(request.json)
    db.session.add(product)
    db.session.commit()
    return {}
