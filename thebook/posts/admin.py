"""Admin part for app posts.
There are 2 classes Group and Post.
"""
from django.contrib import admin

from .models import Book, Comment, Group, Post


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-empty-'


class BookAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author_book', 'description')
    search_fields = ('title', 'author_book',)
    list_filter = ('title', 'author_book',)
    empty_value_display = '-empty-'


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group', 'book')
    list_editable = ('group', 'book')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-empty-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'created', 'author', 'post')
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-empty-'


admin.site.register(Comment, CommentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Post, PostAdmin)
