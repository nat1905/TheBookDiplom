"""Tests for views app posts."""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post
from ..views import PAGES_NUMBER

User = get_user_model()


class PostsViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.group = Group.objects.create(
            title='group',
            slug='slug',
            description='description',
        )
        cls.group_without_post = Group.objects.create(
            title='group without post',
            slug='slug_without_post',
            description='description group without post',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='post',
            group=cls.group,
        )

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(PostsViewsTests.post.author)

    def test_views(self):
        """When use attr name correcponding tempalte HTML is used."""
        templates_url_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group_list', kwargs={'slug': 'slug'}
            ),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': 'user'}
            ),
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': f'{self.post.id}'}
            ),
            'posts/post_create.html': reverse('posts:post_create'),
            'post_edit': reverse(
                'posts:post_edit', kwargs={'post_id': f'{self.post.id}'}
            ),
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.author_client.get(address)
                if address == f'/posts/{self.post.id}/edit/':
                    self.assertTemplateUsed(response, 'posts/post_create.html')
                else:
                    self.assertTemplateUsed(response, template)

    def test_index_gr_list_profile_post_det_correct_context(self):
        """Templates index, group_list, profile, post_detail
        have correct context."""
        templates_url_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group_list', kwargs={'slug': 'slug'}
            ),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': 'user'}
            ),
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': f'{self.post.id}'}
            ),
        }

        for address in templates_url_names.values():
            with self.subTest(address=address):
                response = (self.author_client.get(address))
                self.assertEqual(
                    response.context['post'].group.title, self.post.group.title
                )
                self.assertEqual(
                    response.context['post'].author, self.post.author
                )
                self.assertEqual(response.context['post'].text, self.post.text)

    def test_post_appears_index_group_list_profile(self):
        """Post of one group didn't appear in another one. """
        response = (self.author_client.get(reverse(
            'posts:group_list', kwargs={'slug': 'slug_without_post'}
        )))
        self.assertNotIn(self.post, response.context.get('group').posts.all())


class PaginatorViewsTest(TestCase):
    """Paginator testing for index, profile, group_list"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='username')
        cls.group = Group.objects.create(
            title='group',
            slug='slug',
            description='description',
        )
        cls.postlist = []

        for i in range(PAGES_NUMBER + 1):
            cls.postlist.append(Post.objects.create(
                text=f'Test_post{i}',
                group=cls.group,
                author=cls.user))

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        """The number of posts at first page
        is equal PAGES_NUMBER."""
        templates_url_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group_list', kwargs={'slug': 'slug'}
            ),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': 'username'}
            ),
        }
        for address in templates_url_names.values():
            with self.subTest(address=address):
                response = (self.author_client.get(address))
                self.assertEqual(len(
                    response.context['page_obj']), PAGES_NUMBER)

    def test_second_page_contains_three_records(self):
        """Assert: at second page must be one post."""
        templates_url_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group_list', kwargs={'slug': 'slug'}
            ),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': 'username'}
            ),
        }
        for address in templates_url_names.values():
            with self.subTest(address=address):
                response = self.author_client.get((address) + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 1)
