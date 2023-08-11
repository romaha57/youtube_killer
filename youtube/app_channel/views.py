from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, DeleteView, CreateView

from app_channel.forms import CreateCommunityPostForm
from app_channel.models import Channel, CommunityPost, CommunityComment
from app_main.models import Video


class ChannelPofileView(DetailView):
    model = Channel
    template_name = 'channel/channel.html'
    pk_url_kwarg = 'channel_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(author=self.object.owner, visibility='public').exclude(is_featured_video=True).order_by('-views')[:10]
        context['video_featured'] = Video.objects.filter(author=self.object.owner, is_featured_video=True).first()

        return context


class ChannelAboutView(DetailView):
    model = Channel
    template_name = 'channel/channel-about.html'
    pk_url_kwarg = 'channel_id'


class ChannelVideosView(DetailView):
    model = Channel
    template_name = 'channel/channel-videos.html'
    pk_url_kwarg = 'channel_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(author=self.object.owner, visibility='public').order_by('-created_at')

        return context


class ChannelCommunityPostView(ListView):
    model = CommunityPost
    template_name = 'channel/channel-community.html'
    context_object_name = 'community_posts'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(channel=self.kwargs.get('channel_id'), is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['channel'] = Channel.objects.get(id=self.kwargs.get('channel_id'))

        return context


class ChannelCommunityPostLikeView(View):

    def get(self, request, com_post_id):
        community_post = CommunityPost.objects.get(id=com_post_id)
        user = request.user

        # убираем лайк, если он уже есть
        if user in community_post.likes.all():
            community_post.likes.remove(user)

        # если есть дизлайк и нажали лайк
        elif user in community_post.dislikes.all():
            community_post.dislikes.remove(user)
            community_post.likes.add(user)

        else:
            community_post.likes.add(user)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ChannelCommunityPostDislikeView(View):

    def get(self, request, com_post_id):
        community_post = CommunityPost.objects.get(id=com_post_id)
        user = request.user

        # убираем дизлайк, если он уже есть
        if user in community_post.dislikes.all():
            community_post.dislikes.remove(user)

        # если есть лайк и нажал дизлайк
        elif user in community_post.likes.all():
            community_post.likes.remove(user)
            community_post.dislikes.add(user)

        else:
            community_post.dislikes.add(user)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ChannelCommunityDetailView(DetailView):
    template_name = 'channel/channel-community-detail.html'
    context_object_name = 'community'

    def get_object(self, queryset=None):
        """Получаем пост в сообществе по id"""

        return get_object_or_404(CommunityPost, id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        """Получаем канал по id"""

        context = super().get_context_data(**kwargs)
        context['channel'] = get_object_or_404(Channel, id=self.kwargs.get('channel_id'))

        return context


class CommunityDeleteCommentView(View):
    def get(self, request, com_id, comment_id):
        comment = CommunityComment.objects.get(id=comment_id)
        channel_id = comment.community_post.channel.id
        comment.delete()
        messages.error(request, 'Комментарий успешно удален')

        return redirect('channel-community-detail', pk=com_id, channel_id=channel_id)


class CommunityCreateCommentView(SuccessMessageMixin, View):
    success_message = 'woooooooooooooow'

    def post(self, request, com_id):
        """Создаем комментарий"""

        author = request.user
        com_post = get_object_or_404(CommunityPost, id=com_id)
        comment_text = request.POST.get('comment')
        CommunityComment.objects.create(
            community_post=com_post,
            author=author,
            text=comment_text
        )
        messages.success(request, 'Комментарий успешно создан')

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class CommunityCommunityPostDeleteView(DeleteView):
    template_name = 'channel/channel-community.html'

    def get_object(self, queryset=None):
        """Удаляем пост в комьюнити"""

        post = CommunityPost.objects.filter(id=self.kwargs.get('com_id')).first()
        if post and (post.channel.owner == self.request.user):
            post.delete()
            messages.error(self.request, 'Пост удален')

    def get_context_data(self, **kwargs):
        """Получаем канал по id"""

        context = super().get_context_data(**kwargs)
        context['channel'] = get_object_or_404(Channel, id=self.kwargs.get('channel_id'))

        return context


class CreateCommunityPostView(CreateView):
    model = CommunityPost
    form_class = CreateCommunityPostForm
    template_name = 'channel/create-post.html'

    def form_valid(self, form):
        """Добавляем привязку к каналу текущего пользователя"""
        form.instance.channel = self.request.user.channel
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправляем на созданный пост"""
        return reverse('channel-community-detail', kwargs={'channel_id': self.object.channel.id,'pk': self.object.id})
