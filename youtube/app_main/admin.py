from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Video, Comment


class VideoImportExportAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'visibility')
    list_filter = ('visibility', 'created_at')
    search_fields = ('title', 'author')
    readonly_fields = ('views',)


class CommentImportExportAdmin(ImportExportModelAdmin):
    list_display = ('id', 'text', 'author', 'video', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('text', 'author')


admin.site.register(Video, VideoImportExportAdmin)
admin.site.register(Comment, CommentImportExportAdmin)
