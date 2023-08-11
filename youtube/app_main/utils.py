from datetime import datetime, timedelta

from app_users.models import User
from .models import Video


def control_time_for_count_views(video: Video) -> None:
    """Контроль времени для добавления просмотра к видео(каждые 5 секунд)"""

    now = datetime.utcnow()

    if video.time_update_view_count.timestamp() <= now.timestamp():
        video.time_update_view_count = now + timedelta(seconds=5)
        video.views += 1
        video.save()


def add_video_in_history(video: Video, user: User) -> None:
    """Добавление видео в истории просмотра для пользователя"""

    user.history_videos.add(video)


