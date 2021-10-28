from jwt import ExpiredSignatureError as _ExpiredSignatureError
from jwt import InvalidTokenError as _InvalidTokenError


class Error(Exception):
    pass


class UserAlreadyExistError(Error):

    def __init__(self):
        self.message = 'User already exists'


class UserDoesNotExistError(Error):

    def __init__(self):
        self.message = "User doesn't exist"


class TokenBlackListedError(Error):

    def __init__(self):
        self.message = 'This token has been added to black list, please login again!'


class NotMatchOrUserDoesNotExistsError(Error):

    def __init__(self):
        self.message = "用户名密码不匹配或者用户不存在"


class TokenMissedError(Error):

    def __init__(self):
        self.message = "Token is not exist, please login!"


class ParameterMissingError(Error):

    def __init__(self):
        self.message = "The parameters has not been setted correctly!"


class PermissionDeniedDataAccessException(Error):

    def __init__(self):
        self.message = "数据访问失败，权限不足"  # Data access failed due to insufficient permissions


class DataRetrievalFailureException(Error):

    def __init__(self):
        self.message = "Data could not be retrieved"


class DBTableFieldValidateException(Error):
    def __init__(self):
        self.message = "DB table field validation failed"


class CreateFailureException(Error):
    def __init__(self, error_msg):
        self.message = "Data create failed",
        self.error_msg = error_msg
        self.duplicate_massage = "字段重复，无法创建相同名称的数据"


class DbCommitFailureException(Error):
    def __init__(self, error_msg):
        self.message = "db commit failed",
        self.error_msg = error_msg
        self.violates_foreign_key_msg = '不能删除已使用的条目'
        self.duplicate_massage = "字段重复，无法创建相同名称的数据"


class AdminUserDeleteException(Error):
    def __init__(self, error_msg):
        self.message = "admin error delete failed",
        self.error_msg = error_msg


class NotActiveUserException(Error):
    def __init__(self, error_msg=None):
        self.message = "用户已被停用",
        self.error_msg = error_msg


class NotLatestCheckOrderRevokeException(Error):
    def __init__(self, error_msg=None):
        self.message = "仅支持撤销最后一张盘点单",
        self.error_msg = error_msg


class PhoneCaptchaNotMatchException(Error):
    def __init__(self, error_msg=None):
        self.message = "验证码不正确",
        self.error_msg = error_msg


class OperateNotValidException(Error):
    def __init__(self, error_msg=None):
        self.message = "操作无效",
        self.error_msg = error_msg


class SkuSnDuplicateException(Error):
    def __init__(self, error_msg=None):
        self.message = "货号重复",
        self.error_msg = error_msg


class SendSmsFailedException(Error):
    def __init__(self, error_msg=None):
        self.message = "发送短信失败",
        self.error_msg = error_msg


class NotRegisterException(Error):
    def __init__(self, error_msg=None):
        self.message = "该手机号尚未注册过,请先注册.",
        self.error_msg = error_msg


class UsernameFormatException(Error):
    def __init__(self, error_msg=None):
        self.message = "用户名格式错误.",
        self.error_msg = error_msg


class PhoneNumberException(Error):
    def __init__(self, error_msg=None):
        self.message = "手机号不正确.",
        self.error_msg = error_msg


class PhoneNumberExistException(Error):
    def __init__(self, error_msg=None):
        self.message = "手机号已被注册.",
        self.error_msg = error_msg


class EmptyResourceException(Error):
    def __init__(self, error_msg=None):
        self.message = "资源不存在.",
        self.error_msg = error_msg


class AdviceOrderCreateFailedException(Error):
    def __init__(self, error_msg=None):
        self.message = "建议订单创建失败",
        self.error_msg = error_msg


class SkuSnNotExistException(Error):
    def __init__(self, error_msg=None):
        self.message = "货号不存在",
        self.error_msg = error_msg


class BaseTypeException(Error):
    def __init__(self, error_msg=None):
        self.message = "类型错误",
        self.error_msg = error_msg


class CouponCodeErrorException(Error):
    def __init__(self, error_msg=None):
        self.message = "兑换码错误",
        self.error_msg = error_msg


ExpiredSignatureError = _ExpiredSignatureError
InvalidTokenError = _InvalidTokenError
