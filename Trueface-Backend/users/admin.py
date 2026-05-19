from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CustomUserAdmin(UserAdmin):
  model = User
  list_display = ["email", "name", "role", "is_staff", "is_active"]
  fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("name", "role")}),)
  add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("name", "role")}),)
  search_fields = ["email", "name", "role"]
  ordering = ["email"]


admin.site.register(User, CustomUserAdmin)
