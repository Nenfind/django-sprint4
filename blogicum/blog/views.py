from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Category, Post
from blog.constants import HOME_PAGE_LIMIT


def post_base_query():
    return Post.objects.select_related(
        'location',
        'author',
        'category',
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    """View function for home page."""
    template = 'blog/index.html'
    post_list = post_base_query()[:HOME_PAGE_LIMIT]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, pk):
    """View function for post detail page."""
    template = 'blog/detail.html'
    post = get_object_or_404(post_base_query(), pk=pk)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    """View function for page of posts from one category."""
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = post_base_query().filter(
        category__slug=category_slug
    )

    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)
