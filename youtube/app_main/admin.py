from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Comment, Video


class VideoImportExportAdmin(ImportExportModelAdmin):
    """Отображение данных о видео"""

    list_display = ('id', 'title', 'author', 'created_at', 'visibility')
    list_filter = ('visibility', 'created_at')
    search_fields = ('title', 'author')
    readonly_fields = ('views',)


class CommentImportExportAdmin(ImportExportModelAdmin):
    """Отображение данных о комментариях к видео"""

    list_display = ('id', 'text', 'author', 'video', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('text', 'author')


admin.site.register(Video, VideoImportExportAdmin)
admin.site.register(Comment, CommentImportExportAdmin)
