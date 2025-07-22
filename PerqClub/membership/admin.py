from django.contrib import admin

# Register your models here.
# membership/admin.py

from django.contrib import admin
from .models import MembershipPlan, PlanFeature, UserMembership

admin.site.register(MembershipPlan)
admin.site.register(UserMembership)
admin.site.register(PlanFeature)