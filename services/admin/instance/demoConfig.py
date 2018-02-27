# services/admin/project/config.py


class BaseConfig:
    """Base configuration"""
    TESTING = False
    USING_DEMO_CONFIG = True


class DevelopmentConfig(BaseConfig):
    """Development configuration"""


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    pass
