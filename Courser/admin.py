from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import (
    CustomUserCreationForm,
    CustomEditProfileForm
)
from . import models


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'address', 'city', 'zip_code', 'phone_number')}),
        ('Pyment info', {'fields': ('credit_card_number', 'credit_card_expire_date', 'credit_card_cvv')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    form = CustomEditProfileForm
    model = models.CustomUser
    list_display = ['username', 'email']


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Author)
admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.Course)
admin.site.register(models.CourseLevel)
