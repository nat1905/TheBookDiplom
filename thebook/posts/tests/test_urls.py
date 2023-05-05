from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.user_not_author = User.objects.create_user(username='HasNoName')
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

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_not_author)
        self.author_client = Client()
        self.author_client.force_login(PostsURLTests.post.author)

    def test_templates(self):
        """Доступ к шаблону в зависимости от пользователя."""
        templates_url_names = [
            ['/', self.client, 'posts/index.html'],
            ['/', self.authorized_client, 'posts/index.html'],
            ['/', self.author_client, 'posts/index.html'],
            ['/group/slug/', self.client, 'posts/group_list.html'],
            ['/group/slug/', self.authorized_client, 'posts/group_list.html'],
            ['/group/slug/', self.author_client, 'posts/group_list.html'],
            ['/profile/user/', self.client, 'posts/profile.html'],
            ['/profile/user/', self.authorized_client, 'posts/profile.html'],
            ['/profile/user/', self.author_client, 'posts/profile.html'],
            [f'/posts/{self.post.id}/', self.client, 'posts/post_detail.html'],
            [f'/posts/{self.post.id}/',
                self.authorized_client, 'posts/post_detail.html'],
            [f'/posts/{self.post.id}/',
                self.author_client, 'posts/post_detail.html'],
            ['/create/', self.author_client, 'posts/post_create.html'],
            ['/create/', self.authorized_client, 'posts/post_create.html'],
            [f'/posts/{self.post.id}/edit/',
                self.author_client, 'posts/post_create.html'],
        ]

        for i in templates_url_names:
            address = i[0]
            with self.subTest(address=address):
                response = i[1].get(address)
                self.assertTemplateUsed(response, i[2])

    def test_status_code(self):
        """Тестирование статус кодов доступа к странице в
        зависимости от пользователя."""
        templates_url_names = [
            ['/', self.client, HTTPStatus.OK],
            ['/', self.authorized_client, HTTPStatus.OK],
            ['/', self.author_client, HTTPStatus.OK],
            ['/group/slug/', self.client, HTTPStatus.OK],
            ['/group/slug/', self.authorized_client, HTTPStatus.OK],
            ['/group/slug/', self.author_client, HTTPStatus.OK],
            ['/profile/user/', self.client, HTTPStatus.OK],
            ['/profile/user/', self.authorized_client, HTTPStatus.OK],
            ['/profile/user/', self.author_client, HTTPStatus.OK],
            [f'/posts/{self.post.id}/', self.client, HTTPStatus.OK],
            [f'/posts/{self.post.id}/', self.authorized_client, HTTPStatus.OK],
            [f'/posts/{self.post.id}/', self.author_client, HTTPStatus.OK],
            ['/create/', self.author_client, HTTPStatus.OK],
            ['/create/', self.authorized_client, HTTPStatus.OK],
            [f'/posts/{self.post.id}/edit/',
                self.author_client, HTTPStatus.OK],
            ['/unexpected/', self.client, HTTPStatus.NOT_FOUND],
            ['/unexpected/', self.authorized_client, HTTPStatus.NOT_FOUND],
            ['/unexpected/', self.author_client, HTTPStatus.NOT_FOUND],
        ]

        for i in templates_url_names:
            address = i[0]
            with self.subTest(address=address):
                response = i[1].get(address)
                self.assertEqual(response.status_code, i[2])

    def test_redirects(self):
        """Тестирование redirects."""
        templates_url_names = [
            ['/create/', self.client, ('/auth/login/?next=/create/')],
            [f'/posts/{self.post.id}/edit/', self.client, (
                f'/auth/login/?next=/posts/{self.post.id}/edit/'
            )],
            [f'/posts/{self.post.id}/edit/',
                self.authorized_client, (f'/posts/{self.post.id}/')],
        ]

        for i in templates_url_names:
            address = i[0]
            with self.subTest(address=address):
                response = i[1].get(address)
                self.assertRedirects(response, i[2])
