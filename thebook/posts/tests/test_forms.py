
from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post

User = get_user_model()


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.user_not_author = User.objects.create_user(username='HasNoName')
        cls.guest_user = User.objects.create_user(username='guest')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
        )
        cls.form = PostForm

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(self.user)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_not_author)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
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
        """Валидная форма меняет запись в Post."""
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
        """Не автор не может менять запись в Post."""
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
        """Неавтроизованный пользователь не может создать запись в Post."""
        posts_count = Post.objects.count()
        form_data = {
            'author': self.guest_user,
            'text': 'Тестовый текст_guest_client',
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
        """Шаблоны post_create, post_edit сформированы
        с правильным контекстом."""
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
