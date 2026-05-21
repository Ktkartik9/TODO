from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "priority", "is_completed", "due_date", "created_at")
    list_filter = ("is_completed", "priority", "due_date")
    search_fields = ("title", "description")
    