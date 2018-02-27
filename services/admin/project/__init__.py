# services/admin/project/__init__.py


from flask import Flask, jsonify
import os
import sys


# instantiate the app
app = Flask(__name__)

# mapping from ENVIRONMENT_TYPE to config class name
# ENVIRONMENT_TYPE gets defined in docker-compose-*.yml files
# config class names defined in instance/config.py or instance/demoConfig.py
configTypes = {
        'development': 'DevelopmentConfig',
        'production': 'ProductionConfig',
        'testing': 'TestingConfig',
        }

# Setup configuration.  If there is no admin/instance/config.py file,
# use admin/instance/demoConfig.py instead
configClass = configTypes[os.getenv('ENVIRONMENT_TYPE')]
if 'config.py' in os.listdir(app.instance_path):
    app.config.from_object('instance.config.' + configClass)
else:
    print('No config.py file in instance folder.', file=sys.stderr)
    print('Using demoConfig.py instead', file=sys.stderr)
    app.config.from_object('instance.demoConfig.' + configClass)


@app.route('/admin/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
