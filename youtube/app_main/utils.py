from datetime import datetime, timedelta

from .models import Video


def control_time_for_count_views(video: Video) -> None:
    """Контроль времени для добавления просмотра к видео(каждые 5 секунд)"""

    now = datetime.utcnow()

    if video.time_update_view_count.timestamp() <= now.timestamp():
        video.time_update_view_count = now + timedelta(seconds=5)
        video.views += 1
        video.save()
