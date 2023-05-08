from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from users.models import CustomUser
from .serializers import RegisterUserSerializer, CreateUserSerializer
from .services.services_creation_user import start_creation
from .services.services_registration_user import start_registration
from .services.services_jwt import create_jwt_access_token
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterUser(APIView):
    """Инициализация процесса регистрации"""
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegisterUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validate_data['email']
            username = serializer.validate_data['username']
            start_registration(email, username)
            return Response({
                "email": email,
                "username": username
            })


class CreateUser(APIView):
    """Добавляем нового пользователя в конце регистрации"""
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validate_data['username']
            if start_creation(username):
                user_token = create_jwt_access_token(username)
                return Response({
                    'token': user_token
                })
