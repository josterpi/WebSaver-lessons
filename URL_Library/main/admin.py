from django.contrib import admin
from .models import UserContent


@admin.register(UserContent)
class UserContentAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "user", "created_at")
    list_filter = ("user",)
    search_fields = ("name", "url", "description")
    readonly_fields = ("created_at", "updated_at")
