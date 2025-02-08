from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from blog.models import Comment


class OnlyAuthorMixin(UserPassesTestMixin):
    """Deny a request from anyone but author"""

    def test_func(self):
        """If requesting user is author of content he requests - return True"""
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        return redirect(reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']})
        )


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
