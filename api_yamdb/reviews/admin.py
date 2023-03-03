from django.contrib import admin

from .models import Comment, Review, Title


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'review_id',
        'text',
        'author',
        'pub_date',
    )
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title_id',
        'text',
        'author',
        'score',
        'pub_date',
    )
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
    )
    empty_value_display = '-пусто-'


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
