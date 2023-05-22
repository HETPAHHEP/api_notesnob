from api.models import VerificationCode
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string
from users.models import CustomUser

from notesnob_api.settings import DEFAULT_FROM_EMAIL

CONFIRMATION_CODE_LENGTH = 14


def _set_code_validity_time():
    """Установка времени действительности кода регистрации"""
    code_validity_time = 1  # Время действительности в часах
    current_time = timezone.now()  # Текущее время в осведомленном формате
    code_validity = current_time + timezone.timedelta(hours=code_validity_time)
    return code_validity


def valid_code_check_for_registration(email, username):
    """Проверка существования и действительности кода"""
    user_code = VerificationCode.objects.filter(email=email, username=username)
    if user_code.exists():
        user_code.delete()

    return True


def valid_code_check_for_jwt(code, username):
    """Проверка действительности кода для выдачи JWT"""
    user_code = VerificationCode.objects.get(confirmation_code=code, username=username)
    if user_code:
        # Если код истек, то удаляем его и отправляем новый
        if user_code.expires_at < timezone.now():
            email = user_code.email
            user_code.delete()
            send_email_with_confirmation_code(email, username)
            return False

        user = CustomUser.objects.get(username=username)
        user.is_verified = True  # Сообщает, что JWT токен был выдан
        user_code.delete()
        return True

    return False


def _create_confirmation_code_for_new_user(email, username):
    """Создание код регистрации и добавление его в базу"""
    confirmation_code = get_random_string(CONFIRMATION_CODE_LENGTH)
    VerificationCode.objects.create(
        email=email,
        username=username,
        confirmation_code=confirmation_code,
        expires_at=_set_code_validity_time()
    )

    return confirmation_code


def send_email_with_confirmation_code(user_email, username):
    """Отправление сообщение с кодом регистрации на почту"""
    confirmation_code = _create_confirmation_code_for_new_user(user_email, username)
    subject = 'Код для регистрации NoteSnob'
    message = f'Ваш код для подтверждения регистрации: {confirmation_code}'

    if send_mail(
            subject,
            message,
            DEFAULT_FROM_EMAIL,
            [user_email]):
        return True
