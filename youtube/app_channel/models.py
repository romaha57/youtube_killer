from app_main.models import Video
from app_users.models import User
from django.db import models
from taggit.managers import TaggableManager


def path_for_avatar_channel(instance, filename):
    """Путь для сохранения аватарки канала"""

    return f'user_{instance.owner.email}/avatar/{filename}'


def path_for_community_post_content(instance, filename):
    """Путь для сохранения картинки к посту в сообществе"""

    return f'user_{instance.channel.owner.email}/com_post/{filename}'


class Channel(models.Model):
    """Модель канала"""

    channel_name = models.CharField(max_length=255, verbose_name='название канала')
    full_name = models.CharField(max_length=255, verbose_name='имя')
    description = models.TextField(verbose_name='описание')
    owner = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='владелец канала', related_name='channel')
    keywords = TaggableManager(verbose_name='теги канала')
    subscribers = models.ManyToManyField(User, verbose_name='подписчики', related_name='subscribers',
                                         null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='активный канал')
    avatar = models.ImageField(upload_to=path_for_avatar_channel, verbose_name='аватарка')
    channel_art = models.ImageField(upload_to=path_for_avatar_channel, verbose_name='обложка канала',
                                    null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания канала')
    verified = models.BooleanField(default=False, verbose_name='верифицирован')

    business_email = models.EmailField(null=True, blank=True, verbose_name='почта для сотрудничества')
    is_show_business_email = models.BooleanField(default=False, verbose_name='показывать почту для сотрудничества')

    location = models.CharField(max_length=255, null=True, blank=True, verbose_name='адрес')
    is_show_location = models.BooleanField(default=False, verbose_name='показывать адрес')

    twitter = models.URLField(max_length=255, verbose_name='twitter', null=True, blank=True)
    facebook = models.URLField(max_length=255, verbose_name='facebook', null=True, blank=True)
    instagram = models.URLField(max_length=255, verbose_name='instagram', null=True, blank=True)
    tiktok = models.URLField(max_length=255, verbose_name='tiktok', null=True, blank=True)

    def __str__(self):
        return f'{self.channel_name}'

    def total_views(self):
        """Подсчет общего количества просмотров всех видео канала"""

        total_views_channel = 0
        videos_on_channel = Video.objects.filter(author=self.owner, visibility='public')
        for video in videos_on_channel:
            total_views_channel += video.views

        return total_views_channel

    class Meta:
        verbose_name = 'канал'
        verbose_name_plural = 'каналы'


class CommunityPost(models.Model):
    """Посты в сообществе"""

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name='канал', related_name='community_posts')
    text = models.TextField(verbose_name='описание', null=True, blank=True)
    content = models.FileField(upload_to=path_for_community_post_content, verbose_name='медиа контент',
                               null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    is_active = models.BooleanField(default=True, verbose_name='активен')
    likes = models.ManyToManyField(User, verbose_name='лайки', null=True, blank=True, related_name='likes_com_post')
    dislikes = models.ManyToManyField(User, verbose_name='дизлайки', null=True, blank=True,
                                      related_name='dislikes_com_post')

    def __str__(self):
        return f'{self.text}'[:40]

    class Meta:
        verbose_name = 'пост сообщества'
        verbose_name_plural = 'посты сообщества'


class CommunityComment(models.Model):
    """Комментарии к постам в сообществе"""

    community_post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments',
                                       verbose_name='пост сообщества')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, related_name='community_comments',
                               verbose_name='автор', default=1)
    text = models.TextField(verbose_name='текст комментария')

    def __str__(self):
        return f'{self.community_post.text}'[:50]

    class Meta:
        verbose_name = 'комментарий сообщества'
        verbose_name_plural = 'комментарии сообщества'
