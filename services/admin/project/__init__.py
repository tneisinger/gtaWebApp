# services/admin/project/__init__.py


import os
import sys
import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


# instantiate the app
app = Flask(__name__)

# mapping from ENVIRONMENT_TYPE to config class name
# ENVIRONMENT_TYPE gets defined in docker-compose-*.yml files
# config class names defined in instance/config.py or instance/defaultConfig.py
configTypes = {
        'development': 'DevelopmentConfig',
        'production': 'ProductionConfig',
        'testing': 'TestingConfig',
        }

# Setup configuration.  If there is no admin/instance/config.py file,
# use admin/instance/defaultConfig.py instead
configClass = configTypes[os.getenv('ENVIRONMENT_TYPE')]
if 'config.py' in os.listdir(app.instance_path):
    app.config.from_object('instance.config.' + configClass)
else:
    print('No config.py file in instance folder.', file=sys.stderr)
    print('Using defaultConfig.py instead', file=sys.stderr)
    app.config.from_object('instance.defaultConfig.' + configClass)

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
