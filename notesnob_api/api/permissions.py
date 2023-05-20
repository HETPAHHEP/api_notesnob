from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticatedOrReadOnly


class IsAdminOrReadOnly(BasePermission):
    """Предоставляет доступ только администратору. Иначе только чтение"""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user.is_authenticated and

            (request.user.is_superuser or
             request.user.role == 'admin')
        )


class IsOwnerModeratorAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Предоставляет доступ только администратору, модератору или владельцу.
    Иначе только чтение
    """
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or

            (request.user.is_authenticated and

             (request.user.role == 'moderator' or
              request.user.role == 'admin' or
              obj.author == request.user)
             )
        )


class IsAdminUser(BasePermission):
    """Проверка является ли пользователь администратором"""
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            (request.user.is_superuser or request.user.role == 'admin')
        )
