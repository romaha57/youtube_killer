class TitleMixin:
    """Миксин для title и значения при пустом списке видео"""

    title = None
    empty_list = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.title
        context['empty_list'] = self.empty_list

        return context
