"""Urls for app posts.
"""
from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('books/<int:book_id>/', views.book_posts, name='book_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('books/<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('create_book/', views.book_create, name='book_create'),
    path('books/', views.books, name='books'),
    path(
        'posts/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),
]
