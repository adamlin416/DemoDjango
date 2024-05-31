from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

CustomUser = get_user_model()


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + ((None, {"fields": ("age", "phone")}),)
    list_display = BaseUserAdmin.list_display + ("age", "phone")


if not admin.site.is_registered(CustomUser):
    admin.site.register(CustomUser, UserAdmin)
