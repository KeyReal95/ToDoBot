from django.contrib import admin
from .models import User, Task


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id',
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user',
        'status',
    )
    list_filter = (
        'status',
    )
    search_fields = (
        'id',
        'name',
        'user__telegram_id',
    )
