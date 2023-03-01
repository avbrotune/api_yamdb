from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.models import Genre
from api.serializers import GenreSerializer


class GenreViewSet(
    viewsets.GenericViewSet,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,

):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        slug = self.kwargs.get('pk')
        instance = get_object_or_404(Genre, slug=slug)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

