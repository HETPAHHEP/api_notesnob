from django.core.validators import RegexValidator


class UsernameValidator(RegexValidator):
    """Валидатор допустимого username"""
    regex = r'^[\w.@+-]+\z',
    message = 'Invalid username format'
