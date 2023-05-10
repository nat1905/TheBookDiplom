"""Tests for models app posts."""
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Book, Comment, Group, Post

User = get_user_model()
FIRST_15_CHAR = 15


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='test group',
            slug='slug',
            description='description',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='post',
        )

    def test_models_have_correct_object_names(self):
        """Check that models __str__ works corretly."""
        post = PostModelTest.post
        expected_object_name = post.text[:FIRST_15_CHAR]
        self.assertEqual(expected_object_name, str(post))

        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_verbose(self):
        """Check verbose_name."""
        post = PostModelTest.post
        verbose = post._meta.get_field('text').verbose_name
        self.assertEqual(verbose, 'text')
        verbose = post._meta.get_field('pub_date').verbose_name
        self.assertEqual(verbose, 'pub date')
        verbose = post._meta.get_field('author').verbose_name
        self.assertEqual(verbose, 'author')
        verbose = post._meta.get_field('group').verbose_name
        self.assertEqual(verbose, 'group')

    def test_help_text(self):
        """Check help_text."""
        post = PostModelTest.post
        help_text = post._meta.get_field('text').help_text
        self.assertEqual(help_text, '')
        help_text = post._meta.get_field('group').help_text
        self.assertEqual(help_text, '')


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='test group',
            slug='test slug',
            description='test description',
        )

    def test_models_have_correct_object_names(self):
        """Check that models __str__ works corretly."""
        group = GroupModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_verbose(self):
        """Check verbose_name."""
        group = GroupModelTest.group
        verbose = group._meta.get_field('title').verbose_name
        self.assertEqual(verbose, 'title')
        verbose = group._meta.get_field('slug').verbose_name
        self.assertEqual(verbose, 'slug')
        verbose = group._meta.get_field('description').verbose_name
        self.assertEqual(verbose, 'description')


class BookModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.book = Book.objects.create(
            title='test book',
            author_book='test author',
            description='test description',
        )

    def test_models_have_correct_object_names(self):
        """Check that models __str__ works corretly."""
        book = BookModelTest.book
        expected_object_name = book.title
        self.assertEqual(expected_object_name, str(book))

    def test_verbose(self):
        """Check verbose_name."""
        book = BookModelTest.book
        verbose = book._meta.get_field('title').verbose_name
        self.assertEqual(verbose, 'title')
        verbose = book._meta.get_field('author_book').verbose_name
        self.assertEqual(verbose, 'author book')
        verbose = book._meta.get_field('description').verbose_name
        self.assertEqual(verbose, 'description')


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.comment = Comment.objects.create(
            author=cls.author,
            text='Test comment',
        )

    def test_models_have_correct_object_names(self):
        """Check that models __str__ works corretly."""
        comment = CommentModelTest.comment
        expected_object_name = comment.text[:FIRST_15_CHAR]
        self.assertEqual(expected_object_name, str(comment))

    def test_verbose(self):
        """Check verbose_name."""
        comment = CommentModelTest.comment
        verbose = comment._meta.get_field('text').verbose_name
        self.assertEqual(verbose, 'Text')
        verbose = comment._meta.get_field('author').verbose_name
        self.assertEqual(verbose, 'Author')
        verbose = comment._meta.get_field('post').verbose_name
        self.assertEqual(verbose, 'Post')
