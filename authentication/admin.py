from django.contrib import admin

from authentication.models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    # Django lai default ordering 'email' field bata gara bhannye:
    ordering = ('email',)
    
    # Dashboard list layout ma k k columns dekhaune field list specified garne:
    list_display = ('email', 'is_staff', 'is_superuser')

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)