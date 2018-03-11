# services/flask/project/__init__.py


import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


# Helper predicate that determines if there is a config.py file
# in the instance folder.
def custom_config_file_exists(app):
    return 'config.py' in os.listdir(app.instance_path)


# Helper function to set app configuration.  If there is no
# instance/config.py file, use instance/defaultConfig.py instead
def set_app_configuration(config_class, app):
    if custom_config_file_exists(app):
        app.config.from_object('instance.config.' + config_class)
    else:
        print('No config.py file in instance folder.', file=sys.stderr)
        print('Using defaultConfig.py instead', file=sys.stderr)
        app.config.from_object('instance.defaultConfig.' + config_class)


# instantiate the db
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    CORS(app)

    # mapping from ENVIRONMENT_TYPE to config class name. ENVIRONMENT_TYPE gets
    # defined in docker-compose-*.yml files config class names defined in
    # instance/config.py or instance/defaultConfig.py
    config_classes = {
            'development': 'DevelopmentConfig',
            'production': 'ProductionConfig',
            'testing': 'TestingConfig',
            }

    # set config
    config_class = config_classes[os.getenv('ENVIRONMENT_TYPE')]
    set_app_configuration(config_class, app)

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # register blueprints
    from project.admin.api import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})
    return app
