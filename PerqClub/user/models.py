from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=10)
    is_cafe = models.BooleanField(default=False)
    def save(self,*args,**kwargs):
        if self.is_cafe:
            self.is_staff = True
        super().save(*args,**kwargs)

class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=5)
    
    def __str__(self):
        return f"OTP for {self.phone_number} is {self.otp_code}"
    

from django.db import models
from django.conf import settings

class ContactMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.date()})"
