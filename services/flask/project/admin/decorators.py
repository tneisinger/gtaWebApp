from functools import wraps

from flask import jsonify, request

from project.admin.models import User


class users_only(object):
    """
    Check that the client has an auth_token for a valid user.  If so, run the
    decorated route_function.  Optinally pass the user info into the route
    function if pass_user is set to True.
    """

    def __init__(self, pass_user=False):
        self.pass_user = pass_user

    def __call__(self, route_function, **kwargs):

        @wraps(route_function)
        def wrapper(**kwargs):
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_token = auth_header.split(' ')[1]
                decode_response, _ = User.decode_auth_token(auth_token)

                # If the token is invalid, deny access
                if not isinstance(decode_response, int):
                    response_object['message'] = 'Auth token invalid.'
                    return jsonify(response_object), 401

                # If the token is valid, allow access
                user = User.query.filter_by(id=decode_response).first()
                if self.pass_user:
                    return route_function(user, **kwargs)
                else:
                    return route_function(**kwargs)

            # If no auth_header was provided, return an error
            return jsonify(response_object), 401

        return wrapper
