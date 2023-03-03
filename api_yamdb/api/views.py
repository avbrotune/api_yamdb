from rest_framework import (
    viewsets,
    mixins,
    filters,
)
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from api.models import Genre, Category, Title
from api.serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleSerializer_POST_PATCH_DELETE,
    TitleSerializer_GET
)


class GenreViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):

    filter_backends = (filters.SearchFilter,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        slug = self.kwargs.get('pk')
        instance = get_object_or_404(Genre, slug=slug)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        slug = self.kwargs.get('pk')
        instance = get_object_or_404(Category, slug=slug)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
):

    filter_backends = (DjangoFilterBackend,)
    # serializer_class = TitleSerializer
    queryset = Title.objects.all()

    filterset_fields = (
        'category',
        'genre',
        'name',
        'year'
    )

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleSerializer_POST_PATCH_DELETE
        else:
            return TitleSerializer_GET