# services/flask/project/tests/base.py


import os
from flask_testing import TestCase

from project import create_app, db, set_app_configuration


app = create_app()


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
