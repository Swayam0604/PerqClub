from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)

class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=5)
    
    def __str__(self):
        return f"OTP for {self.phone_number} is {self.otp_code}"
    
