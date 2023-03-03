from rest_framework import serializers

from api.models import Genre, Category, Title


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
