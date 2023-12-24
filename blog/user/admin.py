from django.contrib import admin
from user.models import User, Note
from django.contrib.auth.admin import UserAdmin


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = [NoteInline]
    list_display = ('username', 'email', 'note_count')  # Добавляем 'note_count' в список отображаемых полей

    def note_count(self, obj):
        return obj.note_set.count()  # Подсчитываем количество записей у пользователя

    note_count.short_description = 'Количество нот'  # Задаем название колонке


admin.site.register(User, CustomUserAdmin)
admin.site.register(Note)
