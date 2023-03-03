from django.contrib import admin

from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
    )
    empty_value_display = '-пусто-'

admin.site.register(Comment, CommentAdmin)