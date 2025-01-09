from functools import wraps

from flask import request

from simple_webhook import config


def require_api_token(func):
    """
    Ensures that only authorized users can access the decorated function
    :param func:
    :return:
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization").replace('Bearer ', '')
        if token is None or token not in config['auth']['api_tokens']:
            return {'message': 'Invalid token'}, 401, {'Content-Type': 'application/json'}
        return func(*args, **kwargs)

    return decorated_function
