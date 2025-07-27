from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from .models import MembershipPlan, PlanFeature, UserMembership,PaymentRecord

User = get_user_model()


# Custom form to filter only regular users (not cafés)
class UserMembershipForm(forms.ModelForm):
    class Meta:
        model = UserMembership
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserMembershipForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_cafe=False)


class PlanFeatureInline(admin.TabularInline):
    model = PlanFeature
    extra = 1
    autocomplete_fields = ['plan']
    fields = ('feature_text',)
    show_change_link = True


# Admin for MembershipPlan with inline features
@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'is_most_popular')
    list_filter = ('price', 'is_most_popular')
    search_fields = ('name', 'description')
    inlines = [PlanFeatureInline]
    ordering = ('price',)
    fieldsets = (
        (None, {'fields': ('name', 'description', 'price', 'is_most_popular')}),
    )
    save_on_top = True


# Admin for PlanFeature
@admin.register(PlanFeature)
class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = ('plan', 'feature_text')
    list_filter = ('plan',)
    search_fields = ('feature_text', 'plan__name')
    autocomplete_fields = ['plan']
    ordering = ('plan',)
    save_on_top = True


# Admin for UserMembership
@admin.register(UserMembership)
class CustomUserMembershipAdmin(admin.ModelAdmin):
    form = UserMembershipForm
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('plan', 'is_active', 'start_date', 'end_date')
    search_fields = ('user__username', 'plan__name')
    autocomplete_fields = ['user', 'plan']
    ordering = ('-start_date',)
    fieldsets = (
        (None, {'fields': ('user', 'plan')}),
        ('Membership Period', {'fields': ('start_date', 'end_date')}),
        ('Status', {'fields': ('is_active',)}),
    )
    save_on_top = True
    date_hierarchy = 'start_date'

@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'order_id', 'payment_id', 'status', 'timestamp', 'expired')
    list_filter = ('status', 'timestamp', 'plan')
    search_fields = ('user__username', 'order_id', 'payment_id', 'plan__name')
    readonly_fields = ('timestamp',)

    def expired(self, obj):
        """Return True if the payment is expired (older than 5 minutes), else False."""
        expiry_time = obj.timestamp + timedelta(minutes=5)
        return timezone.now() > expiry_time
    expired.boolean = True
    expired.short_description = 'Expired (5 min)'