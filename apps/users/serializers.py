from django.contrib.auth.hashers import make_password
from rest_framework import serializers, status

from common.exception import (
    CustomException,
    CustomValidationError,
    LoginErrorMessages,
    UserValidationMessages,
)
from common.utils import (
    is_password_str_num_included,
    is_valid_email_format,
    is_valid_password_length,
    is_valid_password_strength,
)

from .models import User
from .models import UserToken as Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'email', 'device_id', 'token', 'time_zone', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if not attrs.get('email'):
            raise CustomValidationError(UserValidationMessages.EMAIL_REQUIRED)
        if not attrs.get('password'):
            raise CustomValidationError(UserValidationMessages.PASSWORD_REQUIRED)
        if not attrs.get('name'):
            raise CustomValidationError(UserValidationMessages.NAME_REQUIRED)
        
        return attrs
    
    def validate_email(self, value):
        if not is_valid_email_format(value):
            raise CustomValidationError(UserValidationMessages.EMAIL_FORMAT_INVALID)
        if User.objects.filter(email=value).exists():
            raise CustomException(message=UserValidationMessages.EMAIL_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)

        return value
    
    def validate_password(self, password):
        if not is_password_str_num_included(password):
            raise CustomValidationError(UserValidationMessages.PASSWORD_STR_NUM_REQUIRED)
        if not is_valid_password_length(password):
            raise CustomValidationError(UserValidationMessages.PASSWORD_LENGTH_INVALID)
        if not is_valid_password_strength(password):
            raise CustomValidationError(UserValidationMessages.PASSWORD_STRENGTH_INVALID)

        return password


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=False, allow_null=True)
    password = serializers.CharField(write_only=True, required=False, allow_null=True)
    device_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        device_id = attrs.get('device_id')
        if not email:
            raise CustomValidationError(UserValidationMessages.EMAIL_REQUIRED)
        if not password:
            raise CustomValidationError(UserValidationMessages.PASSWORD_REQUIRED)
        if not device_id:
            raise CustomValidationError(UserValidationMessages.DEVICE_ID_REQUIRED)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CustomException(LoginErrorMessages.WRONG_EMAIL_OR_PASSWORD, status_code=401)
        if not user.check_password(password):
            raise CustomException(LoginErrorMessages.WRONG_EMAIL_OR_PASSWORD, status_code=401)
        
        attrs['user'] = user
        return attrs

        
class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    name = serializers.CharField(required=False)
    device_id = serializers.CharField(write_only=True, required=False)
    device_os = serializers.CharField(write_only=True, required=False)
    device_os_version = serializers.CharField(write_only=True, required=False)
    
    def validate(self, value):
        if 'email' not in value:
            raise CustomValidationError(UserValidationMessages.EMAIL_REQUIRED)
        if 'password' not in value:
            raise CustomValidationError(UserValidationMessages.PASSWORD_REQUIRED)
        if 'name' not in value:
            raise CustomValidationError(UserValidationMessages.NAME_REQUIRED)
        
        return value
    
    def validate_email(self, value):
        if not is_valid_email_format(value):
            raise CustomValidationError(UserValidationMessages.EMAIL_FORMAT_INVALID)
        if User.objects.filter(email=value).exists():
            raise CustomException(message=UserValidationMessages.EMAIL_ALREADY_EXISTS, status_code=status.HTTP_409_CONFLICT)

        return value
    
    def validate_password(self, password):
        if not is_password_str_num_included(password):
            raise CustomValidationError(UserValidationMessages.PASSWORD_STR_NUM_REQUIRED)
        if not is_valid_password_length(password):
            raise CustomValidationError(UserValidationMessages.PASSWORD_LENGTH_INVALID)
        if not is_valid_password_strength(password):
            raise CustomValidationError(UserValidationMessages.PASSWORD_STRENGTH_INVALID)

        return password
