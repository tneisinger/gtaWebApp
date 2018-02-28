# services/flask/project/tests/base.py


import os
from flask_testing import TestCase

from project import create_app, db, set_app_configuration
from project.admin.models import User


app = create_app()


# helper function for adding a user to the db
def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class BaseTestCase(TestCase):
    def create_app(self):
        set_app_configuration('TestingConfig', app)
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
