from django.db import models
from api.validators import validate_year


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.IntegerField(
        validators=[validate_year],
        verbose_name='Год создания'
    )
    description = models.CharField(
        max_length=256,
        null=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
        verbose_name='Жанры произведения',
    )
    category = models.ForeignKey(
        Category,
        related_name='category',
        verbose_name='Категория произведения',
        on_delete=models.CASCADE,
    )
