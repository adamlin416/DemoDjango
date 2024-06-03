from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    """
    Register the custom user model with the admin site.
    """

    fieldsets = BaseUserAdmin.fieldsets + ((None, {"fields": ("age", "phone")}),)
    list_display = BaseUserAdmin.list_display + ("age", "phone")


if not admin.site.is_registered(User):
    admin.site.register(User, UserAdmin)
