from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.validators import GetTokenForUserError
from users.models import CustomUser

from .permissions import IsAdminUser
from .serializers import (CustomUserSerializer, GetJWTUserSerializer,
                          RegisterUserSerializer)
from .services.services_email_code import valid_code_check_for_jwt
from .services.services_jwt import create_jwt_access_token
from .services.services_registration_user import start_registration


class RegisterUser(APIView):
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


class GetJWTUser(APIView):
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
