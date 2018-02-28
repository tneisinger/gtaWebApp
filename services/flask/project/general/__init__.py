# services/flask/project/general/__init__.py

from flask import Blueprint, jsonify, render_template

from project.admin.models import User

general_blueprint = Blueprint('general', __name__,
                              template_folder='./templates')


@general_blueprint.route('/ping', methods=['GET'])
def ping():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@general_blueprint.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)
