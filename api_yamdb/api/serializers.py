from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Comment, Review
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
