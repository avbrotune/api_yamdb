from random import randint

from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Genre, Category, Title
from api.permissions import IsSuperOrIsAdmin, TitlePermission, GenreCategoryPermission
from api.serializers import CategorySerializer, CheckCodeSerializer, CommentSerializer, GenreSerializer, \
    ReviewSerializer, SignupSerializer, TitleSerializer_GET, TitleSerializer_POST_PATCH_DELETE, UserSerializer
from users.models import User


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            # author=self.request.user,
            author=get_object_or_404(User, pk=1),
            # author=User.objects.get(pk=1)
            title_id=self.get_title()
        )


class GenreViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    filter_backends = (filters.SearchFilter,)
    permission_classes = (GenreCategoryPermission,)
    http_method_names = ['get', 'post', 'delete']
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    search_fields = ('name',)
    pagination_class = PageNumberPagination

    def destroy(self, request, *args, **kwargs):
        slug = self.kwargs.get('pk')
        instance = get_object_or_404(Genre, slug=slug)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    filter_backends = (filters.SearchFilter,)
    permission_classes = (GenreCategoryPermission,)
    http_method_names = ['get', 'post', 'delete']
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    search_fields = ('name',)
    pagination_class = PageNumberPagination

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
    queryset = Title.objects.all()
    permission_classes = (TitlePermission,)
    pagination_class = PageNumberPagination

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

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [permissions.AllowAny]
    #     elif self.request.method in ('POST', 'PATCH', 'DELETE'):
    #         return [permissions.IsAdminUser]


class SignupViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):

    def create(self, request):
        permission_classes = (AllowAny,)
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = randint(100000, 999999)
            user, _ = User.objects.get_or_create(
                **serializer.validated_data
            )
            user.confirmation_code = confirmation_code
            user.save()
            header = 'Код подтверждения yamdb.me'
            message = f'Код подтверждения: {confirmation_code}'
            sender_email = 'madwave-krsk@yandex.ru'
            email = serializer.validated_data.get("email")
            send_mail(
                header,
                message,
                sender_email,
                [email]
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckCodeViewSet(viewsets.ModelViewSet):

    def create(self, request):
        serializer = CheckCodeSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=serializer.validated_data.get("username"))
            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperOrIsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "patch", "head", "delete"]
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['username', ]
    pagination_class = PageNumberPagination
    ordering = ['id']

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated], )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
