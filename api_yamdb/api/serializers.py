from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('author', 'review_id', 'pub_date',)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ('author', 'title_id', 'pub_date',)

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id']
            )
            # author = self.context['request'].user
            author = get_object_or_404(User, pk=1),
            if Review.objects.filter(
                author=author,
                title_id=title_id
            ).exists():
                raise serializers.ValidationError(
                    'Нельзя оставить отзыв на одно произведение дважды'
                )
        return data

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class TitleSerializer_POST_PATCH_DELETE(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    id = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

    def get_id(self, obj):
        return obj.id


class TitleSerializer_GET(serializers.ModelSerializer):
    category = CategorySerializer(
        many=False,
        read_only=True
    )
    genre = GenreSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[UnicodeUsernameValidator(), ],
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    def validate(self, data):
        if data.get('username') == "me":
            raise serializers.ValidationError()
        if User.objects.filter(username=data.get('username')) and not User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError()
        if not User.objects.filter(username=data.get('username')) and User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError()
        return data


class CheckCodeSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
    )
    confirmation_code = serializers.IntegerField(
        required=True,
    )

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        if user.confirmation_code == data.get('confirmation_code'):
            return data
        raise serializers.ValidationError()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
