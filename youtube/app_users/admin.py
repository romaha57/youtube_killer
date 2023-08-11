from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import User


class UserImportExportAdmin(ImportExportModelAdmin):
    pass


admin.site.register(User, UserImportExportAdmin)