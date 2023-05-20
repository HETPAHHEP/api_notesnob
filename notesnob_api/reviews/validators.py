from django.utils import timezone
from rest_framework.validators import ValidationError


def validate_year(value):
    """Проверка действительности года выхода произведение"""
    current_year = timezone.now().year
    if value > current_year:
        raise serializers.ValidationError({"error": "This year hasn't arrived yet."})
