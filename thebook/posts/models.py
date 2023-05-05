"""Models for database: Group, Post.
"""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=200)
    author_book = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    image_book = models.ImageField(
        'Image',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts'
    )
    book = models.ForeignKey(
        Book,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts'
    )

    image = models.ImageField(
        'Image',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ['-pub_date', ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    text = models.TextField(verbose_name='Text', max_length=500)
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Date'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Author'
    )
    post = models.ForeignKey(
        Post,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='comments',
        verbose_name='Post'
    )

    class Meta:
        ordering = ['-created', ]

    def __str__(self):
        return self.text[:15]
