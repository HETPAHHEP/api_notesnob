from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import UsernameValidator


class CustomUser(AbstractUser):
    """Модель пользователя с разными ролями"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(max_length=150, validators=[UsernameValidator], unique=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )


