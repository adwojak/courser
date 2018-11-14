from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm
)
from . import models


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'address', 'city', 'zip_code', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    form = CustomUserChangeForm
    model = models.CustomUser
    list_display = ['username', 'email']


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Author)
admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.Course)
admin.site.register(models.CourseLevel)
