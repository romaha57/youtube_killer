from django.db import models
from django.utils.timezone import now
from taggit.managers import TaggableManager

from app_users.models import User


VISIBILITY = (
    ('public', 'открытый'),
    ('private', 'приватный'),
    ('unlisted', 'закрытый'),
    ('member_only', 'только подписчикам')
)


def path_for_video(instance, filename):
    return f'user_{instance.author.email}/{filename}'


class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name='название видео')
    description = models.TextField(verbose_name='описание')
    video = models.FileField(upload_to=path_for_video, verbose_name='видео')
    image = models.ImageField(upload_to=path_for_video, verbose_name='картинка видео')
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY, default='public', verbose_name='доступ')
    views = models.PositiveIntegerField(default=0, verbose_name='просмотры')
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='автор')
    time_update_view_count = models.DateTimeField(default=now(), verbose_name='время обновления просмотра')

    likes = models.ManyToManyField(User, related_name='likes_video', verbose_name='лайки', null=True, blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes_video', verbose_name='дизлайки', null=True, blank=True)

    history_videos = models.ManyToManyField(User, related_name='history_videos', verbose_name='история просмотра', blank=True, null=True)
    saved_user = models.ManyToManyField(User, related_name='saved_videos', verbose_name='сохраненные видео для просмотра позже', null=True, blank=True)

    is_featured_video = models.BooleanField(default=False, verbose_name='главное видео на канале')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'видео'
        verbose_name_plural = 'видео'


class Comment(models.Model):
    text = models.CharField(max_length=500, verbose_name='текст комментария')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='автор комментария')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='видео', related_name='comments')
    is_active = models.BooleanField(default=True, verbose_name='допустимый')

    def __str__(self):
        return f'{self.text}'[:25]

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

