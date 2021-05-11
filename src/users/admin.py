from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .forms import UserCreationForm, UserChangeForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'middle_name', 'last_name', 'password1', 'password2'),
        }),
    )
