from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended User class"""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE_CHOICES = (
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
        (USER, "Пользователь"),
    )

    email = models.EmailField(
        "Электронная почта",
        max_length=254,
        blank=False,
        unique=True
    )
    bio = models.TextField(
        "О себе",
        blank=True,
    )
    role = models.CharField(
        "Права доступа",
        max_length=9,
        choices=ROLE_CHOICES,
        default=USER,
    )
    confirmation_code = models.CharField(
        max_length=50,
        null=True
    )
