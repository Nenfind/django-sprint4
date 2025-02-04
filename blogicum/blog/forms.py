from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment

User = get_user_model()

class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'category',
            'location',
            'pub_date',
            'image',
        )
        widgets = {
            'pub_date': forms.DateInput(
                attrs={'type': 'date',
                       'value': datetime.now().strftime("%Y-%m-%d")
                       }
            ),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = (
            'text',
        )