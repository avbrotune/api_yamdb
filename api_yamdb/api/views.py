from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from api.filters import TitleFilter
from api.permissions import (
    IsSuperOrIsAdmin,
    IsSuperOrIsAdminOrSafe,
    IsSuperUserIsAdminIsModeratorIsAuthor
)
from api.serializers import (
    CategorySerializer,
    CheckCodeSerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleSerializerForGet,
    TitleSerializerForPostPatchDelete,
    UserSerializer
)
from reviews.models import Genre, Category, Title, Review
from users.models import User


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsSuperUserIsAdminIsModeratorIsAuthor,
    )

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.all().order_by('id')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsSuperUserIsAdminIsModeratorIsAuthor,
    )

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class GenreCategoryBaseViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsSuperOrIsAdminOrSafe,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(GenreCategoryBaseViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by('id')


class CategoryViewSet(GenreCategoryBaseViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('id')


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperOrIsAdminOrSafe,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    filterset_fields = (
        'category__slug',
        'genre__slug',
        'name',
        'year'
    )

    def get_serializer_class(self):
        if self.request.method in {'POST', 'PATCH', 'DELETE'}:
            return TitleSerializerForPostPatchDelete
        else:
            return TitleSerializerForGet

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('reviews__score')
        ).order_by('id')


class SignupViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        username = serializer.data['username']
        user, _ = User.objects.get_or_create(email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        header = 'Код подтверждения yamdb.me'
        message = f'Код подтверждения: {confirmation_code}'
        sender_email = 'madwave-krsk@yandex.ru'
        send_mail(
            header,
            message,
            sender_email,
            [email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


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

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
    )
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
