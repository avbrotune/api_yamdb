from django.urls import include, path
from rest_framework import routers

from api.views import CommentViewSet, UserViewSet, ReviewViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)', CommentViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/signup/', include('djoser.urls')),

]