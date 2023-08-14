from django.urls import path

from .views import (ChannelAboutView, ChannelCommunityDetailView,
                    ChannelCommunityPostDislikeView,
                    ChannelCommunityPostLikeView, ChannelCommunityPostView,
                    ChannelPofileView, ChannelVideosView,
                    CommunityCommunityPostDeleteView,
                    CommunityCreateCommentView, CommunityDeleteCommentView,
                    CreateCommunityPostView)

urlpatterns = [
    path('channel-profile/<int:channel_id>/', ChannelPofileView.as_view(), name='channel-profile'),
    path('channel-community/<int:channel_id>/', ChannelCommunityPostView.as_view(), name='channel-community'),
    path('channel-about/<int:channel_id>/', ChannelAboutView.as_view(), name='channel-about'),
    path('channel-videos/<int:channel_id>/', ChannelVideosView.as_view(), name='channel-videos'),
    path('channel-community-detail/<int:channel_id>/<int:pk>/', ChannelCommunityDetailView.as_view(), name='channel-community-detail'),
    path('community-post-like/<int:com_post_id>/', ChannelCommunityPostLikeView.as_view(), name='community-post-like'),
    path('community-post-dislike/<int:com_post_id>/', ChannelCommunityPostDislikeView.as_view(), name='community-post-dislike'),
    path('community-post-delete/<int:pk>/<int:channel_id>/', ChannelCommunityPostDislikeView.as_view(), name='delete-post'),
    path('community-create-comment/<int:com_id>/', CommunityCreateCommentView.as_view(), name='community-create-comment'),
    path('community-delete-comment/<int:com_id>/<int:comment_id>/', CommunityDeleteCommentView.as_view(), name='community-delete-comment'),
    path('channel-community-post-delete/<int:channel_id>/<int:com_id>/', CommunityCommunityPostDeleteView.as_view(), name='channel-community-post-delete'),
    path('create-post/<int:channel_id>/', CreateCommunityPostView.as_view(), name='create-post'),
]
