from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import Post, Comment


class OnlyAuthorMixin(UserPassesTestMixin):
    """Deny a request from anyone but author"""

    def test_func(self):
        """If requesting user is author of content he requests - return True"""
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']})
        )


def my_queryset(model=None, posted=True, comment=False, order=True):
    if not model:
        model = Post.objects
    queryset = model.select_related(
        'location',
        'author',
        'category',
    )
    if posted:
        queryset = queryset.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
    if comment:
        queryset = queryset.annotate(
            comment_count=Count('comments')
        )
    if order:
        queryset = queryset.order_by('-pub_date')
    return queryset


class ChangeCommentMixin:
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        """Get chosen comment or 404"""
        comment = get_object_or_404(
            Comment,
            pk=self.kwargs['comment_id'],
            post__id=self.kwargs['post_id']
        )
        return comment

    def get_success_url(self):
        """On success redirect to parent post"""
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )
