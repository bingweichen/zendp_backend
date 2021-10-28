from flask_restplus import Resource
from functools import wraps
from flask import current_app
from app.common.responses import internal_error


def error_handler(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            current_app.logger.exception(e)
            return internal_error()
        return result

    return decorated


class BaseResource(Resource):
    method_decorators = [error_handler]
