from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Channel, CommunityPost, CommunityComment


class ChannelImportExportAdmin(ImportExportModelAdmin):
    list_display = ('id', 'channel_name', 'owner', 'is_active', 'verified')
    list_filter = ('is_active', 'verified', 'owner', 'keywords')
    search_fields = ('channel_name', 'owner')


class CommunityPostImportExportAdmin(ImportExportModelAdmin):
    list_display = ('channel', 'short_text', 'is_active')
    list_filter = ('is_active', 'created_at', 'channel')
    search_fields = ('text', )

    def short_text(self, obj):
        return obj.text[:50]


class CommunityCommentImportExportAdmin(ImportExportModelAdmin):
    list_display = ('id', 'community_post', 'created_at', 'author')
    list_filter = ('author', 'created_at',)
    search_fields = ('text',)


admin.site.register(Channel, ChannelImportExportAdmin)
admin.site.register(CommunityPost, CommunityPostImportExportAdmin)
admin.site.register(CommunityComment, CommunityCommentImportExportAdmin)
