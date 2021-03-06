# services/flask/project/tests/test_config.py


import os
import unittest
from flask import current_app
from flask_testing import TestCase

from project import (create_app, set_app_configuration,
                     custom_config_file_exists)

app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        set_app_configuration('DevelopmentConfig', app)
        return app

    def test_app_is_development(self):
        if custom_config_file_exists(app):
            self.assertFalse(app.config['SECRET_KEY'] == 'default_secret_key')
        else:
            self.assertTrue(app.config['SECRET_KEY'] == 'default_secret_key')
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_URL')
        )
        self.assertTrue(app.config['DEBUG_TB_ENABLED'])
        self.assertTrue(app.config['BCRYPT_LOG_ROUNDS'] == 4)
        self.assertTrue(app.config['TOKEN_EXPIRE_DAYS_LONG'] == 30)
        self.assertTrue(app.config['TOKEN_EXPIRE_SECONDS_LONG'] == 0)
        self.assertTrue(app.config['TOKEN_EXPIRE_DAYS_SHORT'] == 0)
        self.assertTrue(app.config['TOKEN_EXPIRE_SECONDS_SHORT'] == 600)


class TestTestingConfig(TestCase):
    def create_app(self):
        set_app_configuration('TestingConfig', app)
        return app

    def test_app_is_testing(self):
        if custom_config_file_exists(app):
            self.assertFalse(app.config['SECRET_KEY'] == 'default_secret_key')
        else:
            self.assertTrue(app.config['SECRET_KEY'] == 'default_secret_key')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_TEST_URL')
        )
        self.assertFalse(app.config['DEBUG_TB_ENABLED'])
        self.assertTrue(app.config['BCRYPT_LOG_ROUNDS'] == 4)
        self.assertTrue(app.config['TOKEN_EXPIRE_DAYS_LONG'] == 0)
        self.assertTrue(app.config['TOKEN_EXPIRE_SECONDS_LONG'] == 3)
        self.assertTrue(app.config['TOKEN_EXPIRE_DAYS_SHORT'] == 0)
        self.assertTrue(app.config['TOKEN_EXPIRE_SECONDS_SHORT'] == 1)


class TestProductionConfig(TestCase):
    def create_app(self):
        set_app_configuration('ProductionConfig', app)
        return app

    def test_app_is_production(self):
        if custom_config_file_exists(app):
            self.assertFalse(app.config['SECRET_KEY'] == 'default_secret_key')
        else:
            self.assertTrue(app.config['SECRET_KEY'] == 'default_secret_key')
        self.assertFalse(app.config['TESTING'])
        self.assertFalse(app.config['DEBUG_TB_ENABLED'])
        self.assertTrue(app.config['BCRYPT_LOG_ROUNDS'] == 13)
        self.assertTrue(app.config['TOKEN_EXPIRE_DAYS_LONG'] == 30)
        self.assertTrue(app.config['TOKEN_EXPIRE_SECONDS_LONG'] == 0)
        self.assertTrue(app.config['TOKEN_EXPIRE_DAYS_SHORT'] == 0)
        self.assertTrue(app.config['TOKEN_EXPIRE_SECONDS_SHORT'] == 600)


if __name__ == '__main__':
    unittest.main()
