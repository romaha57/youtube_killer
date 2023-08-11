from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', SearchView.as_view(), name='search'),
    path('liked_videos/', LikedVideos.as_view(), name='liked_videos'),
    path('history-videos/', HistoryVideos.as_view(), name='history-videos'),
    path('upload-video/', UploadVideoView.as_view(), name='upload-video'),
    path('trending/', TrendingView.as_view(), name='trending'),
    path('subscriptions-videos/', SubscriptionVideosView.as_view(), name='subscriptions_videos'),
    path('saved-videos/', SavedVideosView.as_view(), name='saved-videos'),
    path('video-detail/<int:pk>/', VideoDetail.as_view(), name='video-detail'),
    path('tags/<str:slug>/', VideoByTagsView.as_view(), name='tags'),
    path('saved-video/<int:video_id>', SaveVideoView.as_view(), name='save-video'),
    path('save-comment/', SaveCommentView.as_view(), name='save-comment'),
    path('delete-comment/', DeleteCommentView.as_view(), name='delete-comment'),
    path('add_sub/<int:pk>', AddSubView.as_view(), name='add_sub'),
    path('subLoad/<int:pk>', SubLoadView.as_view(), name='subLoad'),
    path('add_like/<int:video_id>', AddLikeView.as_view(), name='add_like'),
    path('add_dislike/<int:video_id>', AddDislikeView.as_view(), name='add_dislike'),
    path('likeLoad/<int:video_id>', LikeLoadView.as_view(), name='likeLoad'),
    path('dislikeLoad/<int:video_id>', DislikeLoadView.as_view(), name='dislikeLoad'),
    path('video-edit/<int:video_id>/', video_edit, name='video-edit'),
    path('video-delete/<int:video_id>/', VideoDeleteView.as_view(), name='video-delete'),
    path('studio/<int:user_id>/', StudioView.as_view(), name='studio')
]
