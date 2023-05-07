from django.urls import path, include


VERSION_API = 'v1'

urlpatterns = [
    path('{VERSION_API}/auth/', include('djoser.urls')),
    path('{VERSION_API}/auth/', include('djoser.urls.jwt'))
]
