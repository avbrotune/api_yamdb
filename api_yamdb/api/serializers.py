from rest_framework import serializers

from api.models import Genre, Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class CategorySerializer(GenreSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )
