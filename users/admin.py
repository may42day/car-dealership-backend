from django.contrib import admin

from users.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin class for UserProfile model.
    Inherits from 'BaseAdmin' admin model.
    """

    list_display = ["username", "role", "email", "is_active", "is_staff"]
    list_filter = ["role", "is_active", "is_staff"]
    search_fields = ["username"]
    date_hierarchy = "date_joined"
