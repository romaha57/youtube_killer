from django import forms

from .models import Video


class UploadVideoForm(forms.ModelForm):
    """Форма добавления видео"""

    class Meta:
        model = Video
        fields = ('title', 'description', 'tags', 'image', 'video', 'visibility', 'is_featured_video')
