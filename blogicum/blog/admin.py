from django.contrib import admin

from .models import Category, Location, Post


class CategoryAdmin(admin.ModelAdmin):
    """Model admin for category"""

    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = (
        'description',
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('title',)
    list_display_links = ('title',)
    empty_value_display = 'не задано'


class PostAdmin(admin.ModelAdmin):
    """Model admin for post"""

    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at',
        'image'
    )
    list_editable = (
        'pub_date',
        'category',
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('author', 'category')
    list_display_links = ('title',)
    empty_value_display = 'не задано'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Location)
