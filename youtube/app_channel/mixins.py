from app_channel.models import Channel


class GetChannelMixin:

    def get_context_data(self, *args, **kwargs):
        """Получаем сам канал"""

        context = super().get_context_data(*args, **kwargs)
        context['channel'] = Channel.objects.get(id=self.kwargs.get('channel_id'))

        return context
