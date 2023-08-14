from django import forms

from .models import CommunityPost


class CreateCommunityPostForm(forms.ModelForm):
    """Форма создания комментариев к постам в сообществе"""

    class Meta:
        model = CommunityPost
        fields = ('text', 'content')
