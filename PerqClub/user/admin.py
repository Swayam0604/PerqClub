from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, OTP 

admin.site.register(CustomUser)

admin.site.register(OTP)