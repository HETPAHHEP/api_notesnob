from django.urls import include, path

from . import views

VERSION_API = 'v1'

urlpatterns = [
    path(f'{VERSION_API}/auth/signup/', views.RegisterUser.as_view(), name='registration_user'),
    path(f'{VERSION_API}/auth/token/', views.GetJWTUser.as_view(), name='creation_token'),
]
