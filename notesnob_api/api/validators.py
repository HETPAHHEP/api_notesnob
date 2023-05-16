from django.core.validators import RegexValidator, BaseValidator
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ValidationError
from rest_framework import status


class UsernameValidator(RegexValidator):
    """Валидатор допустимого username"""
    regex = r'^[\w.@+-]+$'
    message = 'Invalid username format'


class RestrictedUsernameValidator(BaseValidator):
    message = 'Restricted username: me'

    def __init__(self, limit_value='me', message=None, code=None):
        super().__init__(message, code)
        self.limit_value = limit_value

    def __call__(self, value):
        if value == self.limit_value:
            raise ValidationError(detail={'self.code': self.message}, code=self.code)


class GetTokenForNonExistentUserError(ValidationError):
    status_code = status.HTTP_404_NOT_FOUND
