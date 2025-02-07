from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blogicum.settings import PAGE_LIMIT
from .forms import ProfileForm, PostForm, CommentForm
from .models import Category, Post, Comment
from .utils import OnlyAuthorMixin, my_queryset, ChangeCommentMixin

User = get_user_model()


class HomePageView(ListView):
    """Display home page with paginated posts"""

    model = Post
    template_name = 'blog/index.html'
    paginate_by = PAGE_LIMIT

    def get_queryset(self):
        """Get eligible for show posts"""
        return my_queryset(comment=True, order=True)


class CategoryListView(ListView):
    """Display posts in chosen category"""

    model = Post
    template_name = 'blog/category.html'
    paginate_by = PAGE_LIMIT

    def get_category(self):
        """Get category if published, if not get 404"""
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return category

    def get_queryset(self):
        queryset = my_queryset(
            model=self.get_category().posts,
            comment=True,
            order=True
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class ProfileListView(ListView):
    """Display posts in chosen profile and profile information"""

    template_name = 'blog/profile.html'
    paginate_by = PAGE_LIMIT

    def get_user(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        """Get all posts if requesting user is owner of the profile
        or eligible for show posts otherwise
        """
        if self.request.user.username == self.get_user().get_username():
            queryset = my_queryset(
                posted=False,
                comment=True
            ).filter(author=self.get_user())
        else:
            queryset = my_queryset(
                comment=True
            ).filter(author=self.get_user())
        return queryset

    def get_context_data(self, **kwargs):
        """Add profile data to context"""
        context = super(ProfileListView, self).get_context_data(**kwargs)
        context['profile'] = self.get_user()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Edit user profile"""

    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        """Get profile of requesting user"""
        return self.request.user

    def get_success_url(self):
        """On success redirect to updated profile"""
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostDetailView(DetailView):
    """Display post details and comments"""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        """Get post details, comments and comment form"""
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.select_related('author')
        return context

    def get_object(self, queryset=None):
        post = get_object_or_404(
            my_queryset(posted=False, comment=True), id=self.kwargs['post_id']
        )
        if self.request.user != post.author:
            post = get_object_or_404(
                my_queryset(comment=True), id=self.kwargs['post_id']
            )
        return post


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new post"""

    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        """Validate form data"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """On success redirect to profile page"""
        user = self.request.user
        return reverse('blog:profile', kwargs={'username': user.username})


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    """Edit an existing post"""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        """On success redirect to edited post"""
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    """Delete an existing post"""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        """On success redirects back to home page"""
        return reverse('blog:index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Create a new comment on a post"""

    post_obj = None
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        """Validate form data"""
        form.instance.author = self.request.user
        self.post_obj = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.post = self.post_obj
        return super().form_valid(form)

    def get_success_url(self):
        """On success redirect to parent post"""
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.post_obj.pk}
        )


class CommentUpdateView(OnlyAuthorMixin, ChangeCommentMixin, UpdateView):
    """Edit comment on a post"""

    form_class = CommentForm


class CommentDeleteView(OnlyAuthorMixin, ChangeCommentMixin, DeleteView):
    """Delete comment on a post"""

    model = Comment


class ProfileCreateView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm

    def get_success_url(self):
        """On success redirect to home page"""
        return reverse('blog:index')
