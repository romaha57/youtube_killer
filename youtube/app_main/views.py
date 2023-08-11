import datetime
import time

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView, CreateView, FormView, UpdateView
from taggit.models import Tag

from app_channel.forms import CreateCommunityPostForm
from .forms import UploadVideoForm
from app_channel.models import Channel
from .models import Video, Comment
from .utils import control_time_for_count_views, add_video_in_history


class IndexView(ListView):
    model = Video
    context_object_name = 'videos'
    template_name = 'index.html'
    ordering = '-created_at'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(visibility='public')


class VideoDetail(DetailView):
    model = Video
    context_object_name = 'video'
    template_name = 'video-detail.html'

    def __init__(self):
        super().__init__()
        self.video_tags_id = []

    def get_object(self, queryset=None):
        """Получаем теги для отображения подобных видео справа"""

        video = super().get_object()
        control_time_for_count_views(video=video)
        if self.request.user.is_authenticated:
            self.request.user.history_videos.add(video)
        self.video_tags_id = [video_tag.id for video_tag in video.tags.all()]

        return video

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['similar_videos'] = set(Video.objects.filter(tags__in=self.video_tags_id).exclude(id=self.object.id))
        context['comments'] = Comment.objects.filter(is_active=True, video=self.object).order_by('-created_at')
        context['channel'] = Channel.objects.get(owner=self.object.author)
        return context


class VideoByTagsView(ListView):
    model = Video
    template_name = 'tags.html'
    context_object_name = 'videos'

    def get_queryset(self):
        """Получаем тег из get-запроса и получаем видео по нему"""

        queryset = super().get_queryset()
        tag_slug = self.kwargs.get('slug')
        tag = Tag.objects.get(slug=tag_slug)

        return queryset.filter(tags__in=[tag])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs.get('slug'))
        return context


class SaveCommentView(View):
    def post(self, request):
        video_id = request.POST.get('id')
        video = Video.objects.get(pk=video_id)
        comment_text = request.POST.get('comment')

        if comment_text:
            Comment.objects.create(
                author=self.request.user,
                text=comment_text,
                video=video
            )
            return HttpResponse('comment was added')

        return HttpResponse('')


@method_decorator(csrf_exempt, name='dispatch')
class DeleteCommentView(View):
    def post(self, request):
        comment_id = request.POST.get('cid')
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        return JsonResponse({"status": 1})


class AddSubView(View):
    def get(self, request, pk):
        channel = Channel.objects.get(pk=pk)
        user = request.user

        if user in channel.subscribers.all():
            channel.subscribers.remove(user)
            return JsonResponse('Подписаться', safe=False, status=200)
        else:
            channel.subscribers.add(user)
            return JsonResponse('Отписаться', safe=False, status=200)


class SubLoadView(View):
    def get(self, request, pk):
        channel = Channel.objects.get(pk=pk)
        sub_list = list(channel.subscribers.values())
        return JsonResponse(sub_list, safe=False, status=200)


class AddLikeView(View):
    def get(self, request, video_id):
        video = Video.objects.get(pk=video_id)
        user = request.user

        if user in video.likes.all():
            video.likes.remove(user)
            return JsonResponse('', safe=False, status=200)

        elif user in video.dislikes.all():
            video.dislikes.remove(user)
            video.likes.add(user)
            return JsonResponse('', safe=False, status=200)

        else:
            video.likes.add(user)
            return JsonResponse('', safe=False, status=200)


class LikeLoadView(View):
    def get(self, request, video_id):
        video = Video.objects.get(pk=video_id)
        likes_list = list(video.likes.values())
        return JsonResponse(likes_list, safe=False, status=200)


class AddDislikeView(View):
    def get(self, request, video_id):
        video = Video.objects.get(pk=video_id)
        user = request.user

        if user in video.dislikes.all():
            video.dislikes.remove(user)
            return JsonResponse('', safe=False, status=200)

        elif user in video.likes.all():
            video.likes.remove(user)
            video.dislikes.add(user)
            return JsonResponse('', safe=False, status=200)

        else:
            video.dislikes.add(user)
            return JsonResponse('', safe=False, status=200)


class DislikeLoadView(View):
    def get(self, request, video_id):
        video = Video.objects.get(pk=video_id)
        dislikes_list = list(video.dislikes.values())
        return JsonResponse(dislikes_list, safe=False, status=200)


class SearchView(ListView):
    model = Video
    template_name = 'search.html'
    context_object_name = 'videos'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_param = self.request.GET.get('q')
        return queryset.filter(Q(title__icontains=search_param) | Q(description__icontains=search_param),
                               visibility='public').order_by('-views')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')

        return context


class LikedVideos(ListView):
    template_name = 'trending_saved_liked_subscription_videos.html'
    context_object_name = 'videos'

    def get_queryset(self):
        """Получаем все лайкнутые видео текущего пользователя"""

        return self.request.user.likes_video.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Понравившиеся видео'
        context['empty_list'] = 'Вы не лайкнули ни одного видео'

        return context


class UploadVideoView(CreateView):
    model = Video
    template_name = 'channel/upload-video.html'
    form_class = UploadVideoForm

    def form_valid(self, form):
        """Добавляем автора видео"""

        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('video-detail', kwargs={'pk': self.object.id})


def video_edit(request, video_id):
    video = Video.objects.get(id=video_id)
    user = request.user

    if request.method == 'POST':
        form = UploadVideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.author = user
            new_form.save()
            form.save_m2m()
            messages.success(request, 'Информация обновлена')
            return redirect(reverse('video-detail', kwargs={'pk': video.id}))
    else:
        form = UploadVideoForm(instance=video)
    context = {
        'form': form,
        'video': video,
    }
    return render(request, "channel/upload-video.html", context)


class TrendingView(ListView):
    model = Video
    template_name = 'trending_saved_liked_subscription_videos.html'
    context_object_name = 'videos'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(visibility='public').order_by('-views', '-created_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Тренды'
        context['empty_list'] = 'Список трендов пока пуст'

        return context


class SubscriptionVideosView(ListView):
    template_name = 'trending_saved_liked_subscription_videos.html'
    context_object_name = 'videos'

    def get_queryset(self):
        my_channels_in_subscription = []
        all_channels = Channel.objects.filter(is_active=True)
        for channel in all_channels:
            if self.request.user in channel.subscribers.all():
                my_channels_in_subscription.append(channel)

        my_subscription_channel_author_list = [channel.owner for channel in my_channels_in_subscription]
        videos = Video.objects.filter(author__in=my_subscription_channel_author_list, visibility='public')

        return videos

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Мои подписки'
        context['empty_list'] = 'Нет ни одного видео ваших подписок'

        return context


class SaveVideoView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        user = request.user

        if user in video.saved_user.all():
            video.saved_user.remove(user)
        else:
            video.saved_user.add(request.user)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SavedVideosView(ListView):
    template_name = 'trending_saved_liked_subscription_videos.html'
    context_object_name = 'videos'

    def get_queryset(self):
        return self.request.user.saved_videos.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Сохраненные видео'
        context['empty_list'] = 'Нет ни одного сохраненного видео'

        return context


class HistoryVideos(ListView):
    template_name = 'trending_saved_liked_subscription_videos.html'
    context_object_name = 'videos'

    def get_queryset(self):
        return self.request.user.history_videos.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'История просмотра'
        context['empty_list'] = 'История пока пуста...'

        return context


class StudioView(TemplateView):
    template_name = 'useradmin/studio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['channel'] = Channel.objects.filter(owner=self.request.user).first()
        context['videos'] = Video.objects.filter(author=self.request.user)

        return context


class VideoDeleteView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        video.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


