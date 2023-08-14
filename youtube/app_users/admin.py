from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import User


class UserImportExportAdmin(ImportExportModelAdmin):
    """Отображение данных пользователя"""

    list_display = ('id', 'email')
    search_fields = ('id', 'email')


admin.site.register(User, UserImportExportAdmin)
