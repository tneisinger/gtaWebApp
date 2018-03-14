from functools import wraps

from flask import jsonify, request

from project.admin.models import User


class check_user_is_admin(object):
    """
    Check that the current user has an auth_token for a user that is_admin.
    If so, run the decorated route_function
    """

    def __init__(self, pass_user=False):
        self.pass_user = pass_user

    def __call__(self, route_function):

        @wraps(route_function)
        def wrapper():
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_token = auth_header.split(' ')[1]
                resp = User.decode_auth_token(auth_token)

                # If the token is invalid, deny access
                if not isinstance(resp, int):
                    return jsonify(response_object), 401

                # If the token is valid and the user is_admin, allow access
                user = User.query.filter_by(id=resp).first()
                if user.is_admin:
                    if self.pass_user:
                        return route_function(user)
                    else:
                        return route_function()
                else:
                    # Tell the user that he/she must be admin
                    response_object['message'] = 'User must be admin.'
                    return jsonify(response_object), 401

            # If the user is not signed in or isn't admin, deny access
            return jsonify(response_object), 401

        return wrapper
