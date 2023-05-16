import datetime

from api.models import VerificationCode
from users.models import CustomUser


def _delete_code_info(username, code):
    """Удаление кода регистрации и информации о пользователе"""
    VerificationCode.objects.filter(username=username, confirmation_code=code).delete()


def _check_info_and_create(username, email):
    """Проверка действительности информации о пользователе и создание профиля"""
    user_code = VerificationCode.objects.filter(
        username=username, email=email)
    user = CustomUser.objects.filter(
        username=username, email=email)

    if user_code.exists() and (user_code.first().expires_at.replace(tzinfo=None) < datetime.datetime.now()):
        _delete_code_info(username, code)
        return False

    elif user_code.exists() and not CustomUser.objects.filter(username=username).exists():
        email = user_code.first().email
        _delete_code_info(username, code)
        return True

    return False


def start_creation(username, code):
    """Инициализация процесса создания нового пользователя"""
    if _check_info_and_create(username, code):
        return True
