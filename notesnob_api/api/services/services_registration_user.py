import datetime
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from notesnob_api.settings import DEFAULT_FROM_EMAIL
from api.models import VerificationCode

CONFIRMATION_CODE_LENGTH = 6


def _set_code_validity_time():
    """Установка времени действительности кода регистрации"""
    code_validity_time = 1
    return datetime.datetime.now() + datetime.timedelta(
        hours=code_validity_time
    )


def _valid_code_check(email, username):
    """Проверка существования и действительности кода"""
    unregister_user_code = VerificationCode.objects.filter(email=email, username=username)
    if unregister_user_code.exists():
        # Если код истек, то удаляем его и отправляем новый
        if unregister_user_code.expires_at < datetime.datetime.now():
            unregister_user_code.delete()
            return True
        return False

    return True


def _create_confirmation_code_for_new_user(email, username):
    """Создание код регистрации и добавление его в базу"""
    confirmation_code = get_random_string(CODE_LENGTH)
    VerificationCode.objects.create(
        email=email,
        username=username,
        confirmation_code=confirmation_code,
        expires_at=_set_code_validity_time()
    )

    return confirmation_code


def _send_email_with_confirmation_code(user_email, username):
    """Отправление сообщение с кодом регистрации на почту"""
    confirmation_code = _create_confirmation_code_for_new_user(user_email, username)
    subject = 'Код для регистрации NoteSnob'
    message = f'Ваш код для подтверждения регистрации: {confirmation_code}'

    send_mail(
        subject,
        message,
        DEFAULT_FROM_EMAIL,
        [user_email]
    )


def start_registration(email, username):
    """Осуществление регистрации нового пользователя"""
    if _valid_code_check(email, username):
        _send_email_with_confirmation_code(email, username)
        return
