from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAnonUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_anonymous()


class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()


class IsModeratorUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() and (request.user.is_staff or request.user.role == 'moderator')


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated() and (request.user.is_superuser() or request.user.role == 'admin')



