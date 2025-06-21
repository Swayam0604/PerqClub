from django.shortcuts import render, get_object_or_404, redirect
from .models import MembershipPlan
# from django.contrib.auth.decorators import login_required
from django.utils import timezone

def membership_plans_view(request):
    plans = MembershipPlan.objects.all().prefetch_related('features')
    return render(request, 'membership.html', {'plans': plans})

# @login_required
# def subscribe_to_plan(request, plan_id):
#     plan = get_object_or_404(MembershipPlan, id=plan_id)

#     # Optional: deactivate any previous active subscriptions
#     UserMembership.objects.filter(user=request.user, is_active=True).update(is_active=False)

#     # Create new subscription
#     UserMembership.objects.create(
#         user=request.user,
#         plan=plan,
#         start_date=timezone.now(),
#         is_active=True
#     )
#     return redirect('membership_success')

def payment_success_view(request):
    return render(request, 'payment_success.html')