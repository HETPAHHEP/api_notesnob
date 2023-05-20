from django.urls import include, path
from rest_framework import routers

from . import views

VERSION_API = 'v1'


router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename='users')
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'genres', views.GenreViewSet, basename='genres')
router.register(r'titles', views.TitleViewSet, basename='titles')

router.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                views.CommentViewSet, basename='comments')


urlpatterns = [
    path(f'{VERSION_API}/', include(router.urls)),

    path(f'{VERSION_API}/auth/signup/', views.RegisterUserView.as_view(), name='registration_user'),
    path(f'{VERSION_API}/auth/token/', views.GetJWTUserView.as_view(), name='creation_token'),
]
