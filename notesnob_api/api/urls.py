from django.urls import include, path
from rest_framework import routers

from . import views

VERSION_API = 'v1'


router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename='users')

urlpatterns = [
    path(f'{VERSION_API}/', include(router.urls)),
    path(f'{VERSION_API}/auth/signup/', views.RegisterUser.as_view(), name='registration_user'),
    path(f'{VERSION_API}/auth/token/', views.GetJWTUser.as_view(), name='creation_token'),
]
