from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, CheckCodeViewSet, GenreViewSet, SignupViewSet, TitleViewSet, UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(
    r'genres',
    GenreViewSet,
    basename='genres'
)
router.register(
    r'categories',
    CategoryViewSet,
    basename='categories'
)
router.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)


urlpatterns = [
    path('auth/signup/', SignupViewSet.as_view({'post': 'create'})),
    path('auth/token/', CheckCodeViewSet.as_view({'post': 'create'})),
    path('', include(router.urls)),
]
