from django.core import validators
from django.utils import timezone
from rest_framework.validators import ValidationError


class SlugValidator(validators.RegexValidator):
    """Валидатор для проверки поля slug"""
    regex = r'^[-a-zA-Z0-9_]+$'
    message = 'Slug must only contain letters, numbers, dashes, and underscores.'


class ActualYearValidator:
    """Для проверки правильности года произведения"""
    message = "This year hasn't arrived yet."

    def __call__(self, title_year):
        current_year = timezone.now().year
        if title_year > current_year:  # Год произведения не может быть больше нынешнего
            raise ValidationError(detail={'error': message})
