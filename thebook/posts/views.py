"""Views for app posts.
"""
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm, CommentForm, PostForm
from .models import Book, Group, Post, User

PAGES_NUMBER = 2


def user_author(request, author):
    if request.user != author:
        return False
    return True


def is_user_author(request, author):
    return request.user != author


def paginator(request, posts, pages_numder):
    paginator = Paginator(posts, pages_numder)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    """Main page with list of posts.
    """
    template = 'posts/index.html'
    title = 'Last changes.'
    posts = Post.objects.all()
    page_obj = paginator(request, posts, PAGES_NUMBER)
    context = {
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def books(request):
    """All books.
    """
    template = 'posts/books.html'
    title = 'All books.'
    books = Book.objects.all()
    page_obj = paginator(request, books, PAGES_NUMBER)
    context = {
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


# Guests page
def group_posts(request, slug):
    """Group page.
    """
    template = 'posts/group_list.html'
    title = f'Записи сообщества {get_object_or_404(Group, slug=slug)}'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = paginator(request, posts, PAGES_NUMBER)
    context = {
        'title': title,
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def book_posts(request, book_id):
    """Book page.
    """
    template = 'posts/book_list.html'
    title = f'Posts about {get_object_or_404(Book, pk=book_id)}'
    book = get_object_or_404(Book, pk=book_id)
    posts = book.posts.all()
    page_obj = paginator(request, posts, PAGES_NUMBER)
    context = {
        'title': title,
        'book': book,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    """Author page.
    """
    title = (
        f'Профайл пользователя '
        f'{get_object_or_404(User, username=username)}'
    )
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    author_equel_user = user_author(request, author)
    page_obj = paginator(request, posts, PAGES_NUMBER)
    context = {
        'title': title,
        'author': author,
        'num_post_list': posts.count,
        'page_obj': page_obj,
        'author_equel_user': author_equel_user
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Post page."""
    post = get_object_or_404(Post, pk=post_id)
    author_equel_user = user_author(request, post.author)
    form = CommentForm()
    comments = post.comments.all()
    context = {
        'post': post,
        'author_equel_user': author_equel_user,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Post create page.
    """
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'posts/post_create.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', post.author.username)


@login_required
def book_create(request):
    """Book create page.
    """
    form = BookForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'posts/book_create.html', {'form': form})
    book = form.save(commit=False)
    book.author = request.user
    book.save()
    return redirect('posts:profile', book.author.username)


@login_required
def post_edit(request, post_id):
    """Post edit page.
    """
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)
    if not form.is_valid():
        return render(
            request, 'posts/post_create.html', {'form': form, 'is_edit': True}
        )
    form.save()
    return redirect('posts:post_detail', post.pk)


@login_required
def book_edit(request, book_id):
    """Book edit page.
    """
    book = get_object_or_404(Book, id=book_id)

    form = BookForm(request.POST or None,
                    files=request.FILES or None, instance=book)
    if not form.is_valid():
        return render(
            request, 'posts/book_create.html', {'form': form, 'is_edit': True}
        )
    form.save()
    return redirect('posts:profile', request.user.username)


@login_required
def add_comment(request, post_id):
    """Add comment to post."""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)
