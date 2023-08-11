from django import forms

from .models import CommunityPost


class CreateCommunityPostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ('text', 'content')