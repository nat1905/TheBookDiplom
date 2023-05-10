"""Tests for forms app posts."""
from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Comment, Group, Post

User = get_user_model()


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.user_not_author = User.objects.create_user(username='HasNoName')
        cls.guest_user = User.objects.create_user(username='guest')
        cls.group = Group.objects.create(
            title='Test group',
            slug='slug',
            description='Test description',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Test post',
            group=cls.group,
        )
        cls.form = PostForm

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(self.user)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_not_author)

    def test_create_post(self):
        """Valid form creates Post."""
        posts_count = Post.objects.count()
        form_data = {
            'author': self.user,
            'text': 'Тестовый текст1',
            'group': self.group.id,
        }

        response = self.author_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': 'user'}
        ))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(**form_data).exists()
        )

    def test_edit_post(self):
        """Valid form change Post."""
        posts_count = Post.objects.count()
        response = self.author_client.get(
            reverse(
                'posts:post_edit', kwargs={'post_id': f'{self.post.id}'}
            ),
        )

        form_data = {
            'author': self.user,
            'text': 'New text',
            'group': self.group.id,
        }

        response = self.author_client.post(
            reverse(
                'posts:post_edit', kwargs={'post_id': f'{self.post.id}'}
            ),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': f'{self.post.id}'}
        ))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(**form_data).exists()
        )

    def test_edit_post_not_author(self):
        """Not author can't change Post."""
        posts_count = Post.objects.count()
        response = self.authorized_client.get(
            reverse(
                'posts:post_edit', kwargs={'post_id': f'{self.post.id}'}
            ),
        )

        form_data = {
            'author': self.user,
            'text': 'New text111',
            'group': self.group.id,
        }

        response = self.authorized_client.post(
            reverse(
                'posts:post_edit', kwargs={'post_id': f'{self.post.id}'}
            ),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': f'{self.post.id}'}
        ))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertFalse(
            Post.objects.filter(**form_data).exists()
        )

    def test_create_post_guest_client(self):
        """Not auth user can't create Post."""
        posts_count = Post.objects.count()
        form_data = {
            'author': self.guest_user,
            'text': 'Test_text_guest_client',
        }
        response = self.client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, ('/auth/login/?next=/create/'))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertFalse(
            Post.objects.filter(**form_data).exists()
        )

    def test_create_edit_post_page_show_correct_context(self):
        """Templates post_create, post_edit have
        valid context."""
        templates_url_names = {
            'post_create': reverse('posts:post_create'),
            'post_edit': reverse(
                'posts:post_edit', kwargs={'post_id': f'{self.post.id}'}
            ),
        }
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for address in templates_url_names.values():
            with self.subTest(address=address):
                response = (self.author_client.get(address))
                for value, expected in form_fields.items():
                    with self.subTest(value=value):
                        form_field = response.context.get(
                            'form').fields.get(value)
                        self.assertIsInstance(form_field, expected)

    def test_create_comment(self):
        """Valid form create a comment."""
        post = self.post
        comment_count = post.comments.count()
        response = self.authorized_client.get(
            reverse(
                'posts:add_comment', kwargs={'post_id': f'{post.id}'}
            ),
        )
        form_comment_data = {
            'author': self.user_not_author,
            'text': 'comment',
        }
        response = self.authorized_client.post(
            reverse(
                'posts:add_comment', kwargs={'post_id': f'{post.id}'}
            ),
            data=form_comment_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': f'{post.id}'}
        ))
        self.assertEqual(self.post.comments.count(), comment_count + 1)
        self.assertTrue(
            Comment.objects.filter(**form_comment_data).exists()
        )

    def test_create_comment_guest_client(self):
        """Not authorized user can't create a comment."""
        post = self.post
        comment_count = post.comments.count()
        response = self.client.get(
            reverse(
                'posts:add_comment', kwargs={'post_id': f'{post.id}'}
            ),
        )
        form_comment_data = {
            'author': self.guest_user,
            'text': 'comment',
        }
        response = self.client.post(
            reverse(
                'posts:add_comment', kwargs={'post_id': f'{post.id}'}
            ),
            data=form_comment_data,
            follow=True
        )
        self.assertRedirects(response, (
            '/auth/login/?next=/posts/1/comment/'
        ))
        self.assertEqual(self.post.comments.count(), comment_count)
        self.assertFalse(
            Comment.objects.filter(**form_comment_data).exists()
        )
