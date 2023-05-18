from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import VerificationCode
from api.validators import (GetTokenForUserError, RestrictedUsernameValidator,
                            UsernameValidator)
from users.models import CustomUser

from .services.services_email_code import CONFIRMATION_CODE_LENGTH


class RegisterUserSerializer(serializers.Serializer):
    """Сериализатор для регистрации нового пользователя"""
    username = serializers.CharField(max_length=150, validators=[
        UsernameValidator(), RestrictedUsernameValidator()])
    email = serializers.EmailField(max_length=254)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')

        if CustomUser.objects.filter(username=username, email=email).exists() and \
                CustomUser.objects.filter(username=username, email=email).first().is_verified:

            raise serializers.ValidationError(
                detail={'token': 'Токен для этого пользователя уже выдан'})

        if CustomUser.objects.filter(email=email).exists() and not \
                CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                detail={'email': 'Пользователь с таким email уже существует'})

        if not CustomUser.objects.filter(email=email).exists() and \
                CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                detail={'email': 'Пользователь с таким username уже существует'})

        return attrs


class GetJWTUserSerializer(serializers.Serializer):
    """Сериализатор для выдачи токена после регистрации"""
    username = serializers.CharField(max_length=150, validators=[
        UsernameValidator(), RestrictedUsernameValidator()])
    confirmation_code = serializers.CharField(max_length=CONFIRMATION_CODE_LENGTH)

    def validate(self, attrs):
        if not attrs:
            raise ValidationError({'error': 'Значения для токена отсутствуют'})

        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        if not CustomUser.objects.filter(username=username).exists():
            raise GetTokenForUserError(
                detail={'username': 'Пользователь с таким username не существует'}
            )

        if not VerificationCode.objects.filter(
                confirmation_code=confirmation_code, username=username).exists():
            raise serializers.ValidationError(
                detail={'error': 'Недействительные данные'})

        return attrs


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для взаимодействия с информацией о пользователе"""
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']
