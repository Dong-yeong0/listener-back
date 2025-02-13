from enum import Enum

from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler


class UserValidationMessages:
    EMAIL_REQUIRED = '이메일을 입력해 주세요.'
    PASSWORD_REQUIRED = '비밀번호를 입력해 주세요.'
    EMAIL_REQUIRED = '이메일을 입력해 주세요.'
    EMAIL_ALREADY_EXISTS = '이미 사용 중인 이메일 입니다.'
    EMAIL_FORMAT_INVALID = '형식이 잘못되었습니다.'
    PASSWORD_STR_NUM_REQUIRED = '영문, 숫자를 포함해야합니다.'
    PASSWORD_LENGTH_INVALID = '8~16자로 입력하세요.'
    PASSWORD_STRENGTH_INVALID = '소문자, 대문자, 숫자, 특수문자가 포함되어야 합니다.'


class LoginErrorMessages:
    WRONG_EMAIL_OR_PASSWORD = '이메일 혹은 비밀번호를 확인해 주세요'
    WITHOUT_FILED_ERROR = '이메일 혹은 비밀번호를 입력해 주세요.'


class ExceptionLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class CustomException(Exception):
    """
    Superclass for custom exception classes.
    This shouldn't be raised directly, please raise the appropriate exception for the situation.
    """

    def __init__(
        self,
        message,
        log_message=None,
        status_code=500,
        level=ExceptionLevel.INFO,
        payload=None,
    ):
        Exception.__init__(self)
        self.message = message
        self.log_message = log_message
        self.status_code = status_code
        self.level = level
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


class CustomValidationError(CustomException):
    def __init__(self, message):
        self.message = message
        self.status_code = 400
        super().__init__(self.message)
        

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, CustomException):
        return Response({'message': exc.message}, status=exc.status_code)
    
    if isinstance(exc, CustomValidationError):
        return Response({'message': exc.message}, status=400)
    
    if isinstance(exc, NotAuthenticated):
        return Response({'message': '잘못된 접근입니다.'}, status=400)
    
    if isinstance(exc, ValidationError):
        return Response({'message': str(exc)}, status=400)
        
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
        

    return response