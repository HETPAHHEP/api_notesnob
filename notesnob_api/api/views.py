from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api.validators import GetTokenForUserError
from users.models import CustomUser

from .serializers import GetJWTUserSerializer, RegisterUserSerializer
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
