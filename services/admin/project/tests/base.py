# services/admin/project/tests/base.py


import os
from flask_testing import TestCase

from project import app, db, set_app_configuration


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
