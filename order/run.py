import os

from example1.api import User
from order.app import create_app, db

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_CONFIG', 'development'))
    with app.app_context():
        db.create_all()
        # create a development user
        if User.query.get(1) is None:
            u = User(username='quy')
            u.set_password('dz')
            db.session.add(u)
            db.session.commit()
    app.run()
