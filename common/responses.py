def ok(data=None, message=None):
    response = {
        'data': data,
        'message': message
    }
    return response, 200


def created(data=None, message=None):
    response = {
        'data': data,
        'message': message
    }
    return response, 201


def not_modified(message):
    response = {
        'message': message
    }
    return response, 304


def bad_request(message):
    response = {
        'error': 'bad request',
        'message': message
    }
    return response, 400


def unauthorized(message):
    response = {
        'error': 'unauthorized',
        'message': message
    }
    return response, 401


def forbidden(message):
    response = {
        'error': 'forbidden',
        'message': message
    }
    return response, 403


def not_found(message):
    response = {
        'error': 'not found',
        'message': message
    }
    return response, 404


# def not_created(message):
#     response = {
#         'error': 'not found',
#         'message': message
#     }
#     return response, 403

def internal_error():
    response = {
        'error': 'Internal Server Error'
    }
    return response, 500
