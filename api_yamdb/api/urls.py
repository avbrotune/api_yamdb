from django.urls import include, path
from rest_framework import routers

from api.views import CheckCodeViewSet, SignupViewSet, UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('auth/signup/', SignupViewSet.as_view({'post': 'create'})),
    path('auth/token/', CheckCodeViewSet.as_view({'post': 'create'})),
    path('', include(router.urls)),
]
