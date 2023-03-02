from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User


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
