from users.models import CustomUser

from .services_email_code import (send_email_with_confirmation_code,
                                  valid_code_check_for_registration)


def _create_new_user(email, username):
    """Создание нового пользователя"""
    if not CustomUser.objects.filter(email=email, username=username).exists():
        CustomUser.objects.create(email=email, username=username)


def start_registration(email, username):
    """Осуществление регистрации нового пользователя"""
    if valid_code_check_for_registration(email, username):
        if send_email_with_confirmation_code(email, username):
            _create_new_user(email, username)
