from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
class MembershipPlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    is_most_popular = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class UserMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)  # null if still active
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.user.is_cafe:
            raise ValidationError("Cafés cannot have memberships.")
    
         # Only calculate end_date for new memberships
        if self.pk is None and not self.end_date and self.start_date:
            self.end_date = self.start_date + relativedelta(months=1)
    
        super().save(*args, **kwargs)

  

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    class Meta:
        unique_together = ('user', 'plan', 'start_date')  # Prevent duplicates

class PlanFeature(models.Model):
    plan = models.ForeignKey(
        MembershipPlan,
        related_name='features',
        on_delete=models.CASCADE,
        limit_choices_to={},  # You can filter plans here if needed
        verbose_name="Membership Plan"
    )
    feature_text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.plan.name} - {self.feature_text}"

    class Meta:
        unique_together = ('feature_text', 'plan')  # Prevent duplicate features for the same plan

        
class PaymentRecord(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey('MembershipPlan', on_delete=models.CASCADE)
    
    order_id = models.CharField(max_length=100, unique=True)  # Razorpay Order ID (usually starts with 'order_')
    payment_id = models.CharField(max_length=100, blank=True, null=True)  # Razorpay Payment ID (set after payment)
    signature = models.TextField(blank=True, null=True)  # Razorpay signature (used for verification)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.status}"

