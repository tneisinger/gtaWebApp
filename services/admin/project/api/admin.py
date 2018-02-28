# services/admin/project/api/admin.py


from flask import Blueprint, jsonify


admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/admin/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
