from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet

router_v1 = DefaultRouter()
router_v1.register('genres', GenreViewSet, basename='genres')

urlpatterns = [

    path('v1/', include(router_v1.urls)),

]

