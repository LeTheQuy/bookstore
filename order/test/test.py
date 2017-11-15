import unittest

from example1.api import app, db, User
from order.test.test_client import TestClient


class TestAPI(unittest.TestCase):
    default_username = 'quy'
    default_password = 'dz'

    def setUp(self):
        self.app = app
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        u = User(username=self.default_username)
        u.set_password(self.default_password)
        db.session.add(u)
        db.session.commit()
        self.client = TestClient(self.app, u.generate_auth_token(), '')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_customers(self):
        # get list of customers
        rv, json = self.client.get('/customers/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['customers'] == [])

        # add a customer
        rv, json = self.client.post('/customers/', data={'name': 'quy1'})
        self.assertTrue(rv.status_code == 201)
        location = rv.headers['Location']
        rv, json = self.client.get(location)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'quy1')
        rv, json = self.client.get('/customers/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['customers'] == [location])

        # edit the customer
        rv, json = self.client.put(location, data={'name': 'quy2'})
        self.assertTrue(rv.status_code == 200)
        rv, json = self.client.get(location)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'quy2')

    def test_products(self):
        rv, json = self.client.get('/products/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['products'] == [])

        rv, json = self.client.post('/products/',
                                    data={'name': 'prod1'})
        self.assertTrue(rv.status_code == 201)
        location = rv.headers['Location']
        rv, json = self.client.get(location)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'prod1')
        rv, json = self.client.get('/products/')
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['products'] == [location])

        rv, json = self.client.put(location, data={'name': 'product1'})
        self.assertTrue(rv.status_code == 200)
        rv, json = self.client.get(location)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(json['name'] == 'product1')

