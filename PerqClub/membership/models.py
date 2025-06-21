from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone

class MembershipPlan(models.Model):
   
    
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    is_most_popular = models.BooleanField(default=False)
    
    

   

    def __str__(self):
        return self.name

# class UserMembership(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
#     start_date = models.DateField(default=timezone.now)
#     end_date = models.DateField(null=True, blank=True)  # null if still active
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.plan.name}"

#     class Meta:
#         unique_together = ('user', 'plan', 'start_date')  # Prevent duplicates

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
        