from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token

from common.exception import (
    CustomException,
    CustomValidationError,
    UserValidationMessages,
)
from common.utils import (
    is_password_str_num_included,
    is_valid_email_format,
    is_valid_password_length,
    is_valid_password_strength,
)

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'email', 'time_zone', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password
        return super().create(validated_data)
    
    def validate(self, attrs):
        if 'email' not in attrs:
            raise CustomValidationError(UserValidationMessages.EMAIL_REQUIRED)
        if 'password' not in attrs:
            raise CustomValidationError(UserValidationMessages.PASSWORD_REQUIRED)
        if 'name' not in attrs:
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