# services/flask/project/config.py

import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'default_secret_key'
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    BCRYPT_LOG_ROUNDS = 13

    # Length of time for which a token is valid.
    # The LONG constants are for use on devices that the user declares are
    # private, whereas the SHORT constants are for public devices.
    TOKEN_EXPIRE_DAYS_LONG = 30
    TOKEN_EXPIRE_SECONDS_LONG = 0
    TOKEN_EXPIRE_DAYS_SHORT = 0
    TOKEN_EXPIRE_SECONDS_SHORT = 600


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG_TB_ENABLED = True
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRE_DAYS_LONG = 0
    TOKEN_EXPIRE_SECONDS_LONG = 3
    TOKEN_EXPIRE_DAYS_SHORT = 0
    TOKEN_EXPIRE_SECONDS_SHORT = 1


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
