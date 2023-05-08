from api.models import VerificationCode
from users.models import CustomUser


def _delete_code_info(username):
    """Удаление кода регистрации и информации о пользователе"""
    VerificationCode.objects.filter(username=username).delete()


def _create_new_user(username, email):
    """Создание нового пользователя"""
    CustomUser.objects.create(email=email, username=username)


def _check_verification_info_and_create(username):
    """Проверка действительности кода и информации о пользователе"""
    new_user = VerificationCode.objects.filter(username=username)

    if new_user.exists() and CustomUser.objects.filter(username=username).aexists():
        email = new_user.email
        _create_new_user(email=email, username=username)
        _delete_code_info(username)
        return True


def start_creation(username):
    """Инициализация процесса создания нового пользователя"""
    if _check_verification_info_and_create(username=username):
        return True
