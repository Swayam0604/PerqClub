from datetime import timedelta
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from .models import CustomUser, OTP 

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None,                     {'fields': ('username', 'password')}),
        ('Personal info',          {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions',            {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_cafe', 'groups', 'user_permissions')}),
        ('Important dates',        {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'password1', 'password2', 'is_cafe'),
        }),
    )
    list_display = ('username', 'email', 'phone_number', 'is_cafe', 'is_staff', 'is_active')
    list_filter  = ('is_cafe', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields= ('username', 'email', 'phone_number')
    ordering     = ('username',)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display   = ('phone_number', 'otp_code', 'created_at', 'expired')
    list_filter    = ('created_at',)
    search_fields  = ('phone_number', 'otp_code')
    readonly_fields= ('created_at',)

    def expired(self, obj):
        return obj.created_at < timezone.now() - timedelta(minutes=5)
    expired.boolean = True
    expired.short_description = 'Expired'