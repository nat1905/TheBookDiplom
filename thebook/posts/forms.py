"""Forms for app Post.
"""
from django import forms

from .models import Book, Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'book', 'image')
        labels = {
            'text': 'Text of the post',
            'group': 'Group',
            'book': 'Post is about the book',
            'image': 'Upload image'
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author_book', 'description', 'image_book')
        labels = {
            'title': 'Book title',
            'author_book': 'Author of the book',
            'description': 'Description of the book',
            'image_book': 'Upload image'

        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
