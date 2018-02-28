# services/flask/project/general/__init__.py


from flask import Blueprint, jsonify


general_blueprint = Blueprint('general', __name__)

@general_blueprint.route('/ping', methods=['GET'])
def ping():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
