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
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_token = auth_header.split(' ')[1]
                resp = User.decode_auth_token(auth_token)
                user = User.query.filter_by(id=resp).first()
                if user.is_admin:

                    # user is_admin. Let the user use the route
                    if self.pass_user:
                        return route_function(user)
                    else:
                        return route_function()

            # If the user is not signed in or isn't admin, deny access
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return jsonify(response_object), 400

        return wrapper
