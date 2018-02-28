# services/admin/project/tests/test_config.py


import os
import unittest

from flask import current_app
from flask_testing import TestCase

from project import app, set_app_configuration, custom_config_file_exists


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        set_app_configuration('DevelopmentConfig', app)
        return app

    def test_app_is_development(self):
        if custom_config_file_exists(app):
            self.assertFalse(app.config['SECRET_KEY'] == 'my_precious')
        else:
            self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_URL')
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        set_app_configuration('TestingConfig', app)
        return app

    def test_app_is_testing(self):
        if custom_config_file_exists(app):
            self.assertFalse(app.config['SECRET_KEY'] == 'my_precious')
        else:
            self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_TEST_URL')
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        set_app_configuration('ProductionConfig', app)
        return app

    def test_app_is_production(self):
        if custom_config_file_exists(app):
            self.assertFalse(app.config['SECRET_KEY'] == 'my_precious')
        else:
            self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertFalse(app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
