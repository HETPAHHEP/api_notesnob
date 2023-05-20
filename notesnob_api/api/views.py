from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.validators import GetTokenForUserError
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser

from .mixins import CreateListDestroyViewSet
from .permissions import (IsAdminOrReadOnly, IsAdminUser,
                          IsOwnerModeratorAdminOrReadOnly)
from .serializers import (CategorySerializer, CustomUserSerializer,
                          GenreSerializer, GetJWTUserSerializer,
                          RegisterUserSerializer, ReviewSerializer,
                          TitleWriteSerializer, TitleReadSerializer, CommentSerializer)
from .services.services_email_code import valid_code_check_for_jwt
from .services.services_jwt import create_jwt_access_token
from .services.services_registration_user import start_registration
from .filters import TitleFilter


class RegisterUserView(APIView):
    """Инициализация процесса регистрации"""
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']

            start_registration(email, username)
            return Response({
                "email": email,
                "username": username
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetJWTUserView(APIView):
    """Добавляем нового пользователя в конце регистрации"""
    serializer_class = GetJWTUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']

            if valid_code_check_for_jwt(confirmation_code, username):
                user_token = create_jwt_access_token(username)
                return Response({
                    'token': user_token
                })

        try:
            if serializer.errors.get('username')[0] == 'Пользователь с таким username не существует':
                raise GetTokenForUserError(serializer.errors)
        except TypeError:
            raise ValidationError(serializer.errors)

        return Response({
            'serializer_errors': serializer.errors,
            'message': 'Что-то пошло не так.'
        }, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.ModelViewSet):
    """Изменение и просмотр информации пользователей"""
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'username'
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated], url_name='me', url_path='me')
    def profile_info_for_auth_user(self, request):
        """Получить или изменить информацию профиля"""
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(CreateListDestroyViewSet):
    """Просмотр всех категорий"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]


class GenreViewSet(CreateListDestroyViewSet):
    """Просмотр всех жанром"""
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    """Изменение и просмотр всех произведений"""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Изменение и просмотр всех отзывов"""
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerModeratorAdminOrReadOnly]

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Изменение и просмотр всех комментариев к отзывам"""
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerModeratorAdminOrReadOnly]

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
