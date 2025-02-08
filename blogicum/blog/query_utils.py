from django.db.models import Count
from django.utils import timezone

from .models import Post


def base_post_queryset(manager=Post.objects, posted=True, comment=False):
    queryset = manager.select_related(
        'location',
        'author',
        'category',
    ).order_by('-pub_date')
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
    return queryset
