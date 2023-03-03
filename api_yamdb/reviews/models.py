#from django.contrib.auth import get_user_model
from django.db import models

from users.models import User

#User = get_user_model()


class Title(models.Model): 
    text = models.TextField()


class Review(models.Model):
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
        )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
        )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
        )


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
        )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
        )
