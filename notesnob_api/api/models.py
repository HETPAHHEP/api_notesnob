from api.validators import UsernameValidator
from django.db import models

CONFIRMATION_CODE_LENGTH = 14


class VerificationCode(models.Model):
    """Модель для хранения кодов подтверждения регистрации"""
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=150, validators=[UsernameValidator()])
    confirmation_code = models.CharField(max_length=CONFIRMATION_CODE_LENGTH)
    expires_at = models.DateTimeField(blank=False)
