from rest_framework import serializers
from users.models import CustomUser
from users.validators import UsernameValidator
from .services.services_registration_user import CONFIRMATION_CODE_LENGTH
from api.models import VerificationCode


class RegisterUserSerializer(serializers.Serializer):
    """Сериализатор для регистрации нового пользователя"""
    username = serializers.CharField(max_length=150, validators=[UsernameValidator])
    email = serializers.EmailField(max_length=254)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')

        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                detail={'username': 'Пользователь с таким username уже существует'})

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail={'email': 'Пользователь с таким email уже существует'})


class CreateUserSerializer(serializers.Serializer):
    """Сериализатор для создания пользователя после подтверждения регистрации"""
    username = serializers.CharField(max_length=150, validators=[UsernameValidator])
    confirmation_code = serializers.CharField(max_length=CONFIRMATION_CODE_LENGTH)

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                detail={'username': 'Пользователь с таким username уже существует'})

        if VerificationCode.objects.filter(
                confirmation_code=confirmation_code, username=username).aexists():
            raise serializers.ValidationError(
                detail={'error': 'Недействительные данные'})