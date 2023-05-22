from rest_framework_simplejwt.tokens import AccessToken
from users.models import CustomUser


def create_jwt_access_token(username):
    """Создание токена доступа для пользователя"""
    user = CustomUser.objects.get(username=username)
    token = AccessToken.for_user(user)

    return str(token)
