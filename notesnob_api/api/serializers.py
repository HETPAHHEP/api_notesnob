from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import VerificationCode
from api.validators import (GetTokenForUserError, RestrictedUsernameValidator,
                            UsernameValidator)
from reviews.models import Category, Comment, Genre, Review, Title
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

        # if CustomUser.objects.filter(username=username, email=email).exists() and \
        #         CustomUser.objects.filter(username=username, email=email).first().is_verified:
        #     raise serializers.ValidationError(
        #         detail={'token': 'Токен для этого пользователя уже выдан'})

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


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для взаимодействия с категориями произведения"""

    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для взаимодействия с жанрами произведения"""

    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений"""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для взаимодействия с произведениями"""
    genre = serializers.SlugRelatedField(slug_field='slug', many=True, queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для взаимодействия с обзорами произведений"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']

    def validate(self, attrs):
        request = self.context.get('request')

        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            user = request.user

            if Review.objects.filter(author=user, title=title_id).exists():
                raise ValidationError(
                    detail={'error': 'Отзыв от этого пользователя уже был оставлен.'}, )

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для взаимодействия с комментариями"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']
