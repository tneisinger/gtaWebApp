# services/admin/project/__init__.py


import os
import sys
import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


# Helper predicate that determines if there is a config.py file
# in the instance folder.
def custom_config_file_exists(app):
    return 'config.py' in os.listdir(app.instance_path)


# Helper function to set app configuration.  If there is no
# admin/instance/config.py file, use admin/instance/defaultConfig.py instead
def set_app_configuration(config_class, app):
    if custom_config_file_exists(app):
        app.config.from_object('instance.config.' + config_class)
    else:
        print('No config.py file in instance folder.', file=sys.stderr)
        print('Using defaultConfig.py instead', file=sys.stderr)
        app.config.from_object('instance.defaultConfig.' + config_class)


# instantiate the app
app = Flask(__name__)


# mapping from ENVIRONMENT_TYPE to config class name
# ENVIRONMENT_TYPE gets defined in docker-compose-*.yml files
# config class names defined in instance/config.py or instance/defaultConfig.py
config_classes = {
        'development': 'DevelopmentConfig',
        'production': 'ProductionConfig',
        'testing': 'TestingConfig',
        }


# setup config
config_class = config_classes[os.getenv('ENVIRONMENT_TYPE')]
set_app_configuration(config_class, app)

# instantiate the db
db = SQLAlchemy(app)


# model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email


@app.route('/admin/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

