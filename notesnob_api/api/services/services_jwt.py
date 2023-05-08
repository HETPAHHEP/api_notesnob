from rest_framework_simplejwt.tokens import AccessToken


def create_jwt_access_token(username):
    """Создание токена доступа для пользователя"""
    user = {'username': username}
    token = AccessToken.for_user(user)

    return str(token)
