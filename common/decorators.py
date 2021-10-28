from flask import g
from flask import request
from functools import wraps

from common import responses, errors
from common.base_logging import my_error_log
from common.errors import (DataRetrievalFailureException,
                           NotMatchOrUserDoesNotExistsError,
                           UserAlreadyExistError,
                           InvalidTokenError,
                           ExpiredSignatureError,
                           TokenBlackListedError,
                           PermissionDeniedDataAccessException,
                           CreateFailureException,
                           AdminUserDeleteException,
                           DbCommitFailureException
                           )


def arguments_parser(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # save the post or get request param to flask g variable
        if request.method == 'GET':
            get_data = request.args
            g.args_get = get_data if get_data else {}
            g.args = g.args_get
            return func(*args, **kwargs)

        post_data = request.json
        get_data = request.args
        g.args_post = post_data if post_data else {}
        g.args_get = get_data if get_data else {}
        g.args = g.args_post
        g.args.update(g.args_get)
        return func(*args, **kwargs)

    return decorated


def catch_error(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DataRetrievalFailureException as e:
            return responses.not_found(e.message)
        except NotMatchOrUserDoesNotExistsError as e:
            return responses.not_found(e.message)
        except UserAlreadyExistError as e:
            return responses.bad_request(e.message)
        except ExpiredSignatureError:
            return responses.unauthorized('Token is expired, please try to login again!')
        except InvalidTokenError:
            return responses.unauthorized('Invalid token, please try to login again!')
        except TokenBlackListedError as e:
            return responses.unauthorized(e.message)

        except PermissionDeniedDataAccessException as e:
            return responses.unauthorized(e.message)
        except AdminUserDeleteException as e:
            return responses.unauthorized(e.message)
        except CreateFailureException as e:
            my_error_log.logger.error(e.error_msg)
            if "duplicate key value violates unique constraint" in e.error_msg:
                return responses.bad_request(e.duplicate_massage)
            return responses.bad_request(e.error_msg)
        except DbCommitFailureException as e:
            my_error_log.logger.error(e.error_msg)
            if "duplicate key value violates unique constraint" in e.error_msg:
                return responses.bad_request(e.duplicate_massage)
            if 'violates foreign key constraint' in e.error_msg:
                return responses.bad_request(e.violates_foreign_key_msg)
            return responses.bad_request(e.error_msg)
        except errors.NotActiveUserException as e:
            return responses.unauthorized(e.message)
        except errors.PhoneCaptchaNotMatchException as e:
            return responses.bad_request(e.message)

        except errors.OperateNotValidException as e:
            return responses.bad_request(e.message)
        except errors.SkuSnDuplicateException as e:
            return responses.bad_request(e.error_msg)
        except errors.SendSmsFailedException as e:
            return responses.bad_request(e.error_msg)
        except errors.NotRegisterException as e:
            return responses.bad_request(e.message)
        except errors.UsernameFormatException as e:
            return responses.bad_request(e.message)
        except errors.PhoneNumberException as e:
            return responses.bad_request(e.message)
        except errors.PhoneNumberExistException as e:
            return responses.bad_request(e.message)
        except errors.EmptyResourceException as e:
            return responses.bad_request(e.error_msg)
        except errors.AdviceOrderCreateFailedException as e:
            return responses.bad_request(e.error_msg)
        except errors.SkuSnNotExistException as e:
            return responses.bad_request(e.error_msg)
        except errors.NotLatestCheckOrderRevokeException as e:
            return responses.bad_request(e.message)
        except errors.CouponCodeErrorException as e:
            return responses.bad_request(e.error_msg)

    return _wrapper
