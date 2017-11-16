from flask import jsonify, request

from order.app import db, json
from order.app.api_v1 import api
from order.app.decorators.paginate import paginate
from order.app.models import Customer


@api.route('/customers/', methods=['GET'])
@json
@paginate('customers')
def get_customers():
    return Customer.query


@api.route('/customers/<int:id>', methods=['GET'])
@json
def get_customer(id):
    return Customer.query.get_or_404(id).export_data()


@api.route('/customers/', methods=['POST'])
@json
def new_customer():
    customer = Customer()
    customer.import_data(request.json)
    db.session.add(customer)
    db.session.commit()
    return {}, 201, {'Location': customer.get_url()}


@api.route('/customers/<int:id>', methods=['PUT'])
@json
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    customer.import_data(request.json)
    db.session.add(customer)
    db.session.commit()
    return {}
