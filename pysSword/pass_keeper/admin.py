from django.contrib import admin

from .models import PasswordEntry


class PasswordEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user_email', 'date_created', 'last_updated']
    ordering = ['-last_updated']
    list_filter = ['date_created', 'last_updated']
    search_fields = ['title', 'username', 'website', 'user__email']
    search_help_text = 'Поиск клиентов по полям Наименование, Веб-сайт, Логин, Пользователь'
    readonly_fields = ['date_created', 'last_updated']
    fields = ['title', 'website', 'username', 'notes', 'date_created', 'last_updated', 'user']
    list_per_page = 10

    @staticmethod
    def user_email(obj):
        return obj.user.email


admin.site.register(PasswordEntry, PasswordEntryAdmin)
