from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from cafe.models import CafeLocation
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import MembershipPlan, UserMembership,PaymentRecord
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from razorpay.errors import SignatureVerificationError
from django.http import HttpResponseBadRequest,HttpResponseForbidden,JsonResponse
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.core.mail import send_mail


@login_required
def membership_plans_view(request):
    plans = MembershipPlan.objects.all()
    return render(request, 'membership.html', {
        'plans': plans,
    })

@login_required
def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_cafe:
        return HttpResponseForbidden("Cafés cannot subscribe to memberships.")

    # Get selected membership or fallback to first plan
    membership_id = request.GET.get("membership_id") or request.POST.get("plan_id")
    print("ID",membership_id)
    if membership_id:
        membership = get_object_or_404(MembershipPlan, id=membership_id)
    else:
        membership = MembershipPlan.objects.first()

    # Create initial Razorpay order
    amount = int(float(membership.price) * 100)
    data = {
        "amount": amount,
        "currency": "INR",
        "receipt": f"membership_{request.user.id}_{membership.id}",
    }
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    payment_details = client.order.create(data=data)

    # PaymentRecord is created on AJAX order (not here), so not repeated

    context = {
        'memberships': MembershipPlan.objects.all(),
        'current_membership': (UserMembership.objects.filter(user=request.user, is_active=True).first().plan
            if UserMembership.objects.filter(user=request.user, is_active=True).exists()
            else membership),
        'is_upgrade': False,
        'memberships_json': json.dumps([
            {
                'id': m.id,
                'name': m.name,
                'description': m.description,
                'price': float(m.price),
                'perks': [str(feature.feature_text) for feature in m.features.all()],
            } for m in MembershipPlan.objects.all()
        ], cls=DjangoJSONEncoder),
        "payment_details": payment_details,
    }
    return render(request, 'checkout.html', context)

@require_GET
@login_required
def create_razorpay_order(request, membership_id):
    membership = get_object_or_404(MembershipPlan, id=membership_id)
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    order_data = {
        "amount": int(float(membership.price) * 100),
        "currency": "INR",
        "payment_capture": "1"
    }
    razorpay_order = client.order.create(data=order_data)
    # Create PaymentRecord with 'pending' status
    PaymentRecord.objects.create(
        user=request.user,
        plan=membership,
        order_id=razorpay_order['id'],
        status='pending'
    )
    return JsonResponse({"order_id": razorpay_order['id']})

@csrf_exempt
def membership_payment_success(request):
    if not request.user.is_authenticated or request.user.is_cafe:
        return HttpResponseForbidden("Cafés cannot complete membership payments.")

    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method.")

    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_signature = request.POST.get("razorpay_signature")
    plan_id = request.POST.get("plan_id")

    if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature, plan_id]):
        return HttpResponseBadRequest("Missing payment data or plan ID.")

    try:
        plan = MembershipPlan.objects.get(id=plan_id)
    except MembershipPlan.DoesNotExist:
        return HttpResponseBadRequest("Invalid membership plan selected.")

    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
        })
        payment_status = 'success'
    except SignatureVerificationError:
        payment_status = 'failed'
        PaymentRecord.objects.filter(order_id=razorpay_order_id).update(status='failed')
        # Send failure email
        send_mail(
            subject="Membership Purchase Failed",
            message=f"Dear {request.user.get_full_name() or request.user.username},\n\nYour membership payment for {plan.name} failed. Please try again or contact support.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=True,
        )
        return render(request, "payment_failed.html")

    payment_record, created = PaymentRecord.objects.get_or_create(
        order_id=razorpay_order_id,
        defaults={
            'user': request.user,
            'plan': plan,
            'status': 'pending'
        }
    )
    payment_record.payment_id = razorpay_payment_id
    payment_record.signature = razorpay_signature
    payment_record.status = payment_status
    payment_record.paid_at = timezone.now()
    payment_record.save()

    if payment_status != 'success':
        return render(request, "payment_failed.html")

    # Membership activation logic
    today = timezone.now().date()
    duration = getattr(plan, 'duration_months', 1)  # Default to 1 month if not defined

    with transaction.atomic():
        active_membership = UserMembership.objects.filter(
            user=request.user, is_active=True, end_date__gte=today
        ).first()

        if active_membership:
            if active_membership.plan == plan:
                # Extend current membership
                base_date = max(active_membership.end_date, today)
                active_membership.end_date = base_date + relativedelta(months=duration)
                active_membership.save()
            else:
                # Deactivate old, activate new
                active_membership.is_active = False
                active_membership.deactivated_at = timezone.now()
                active_membership.save()

                UserMembership.objects.create(
                    user=request.user,
                    plan=plan,
                    start_date=today,
                    end_date=today + relativedelta(months=duration),
                    is_active=True
                )
        else:
            # First time membership
            UserMembership.objects.create(
                user=request.user,
                plan=plan,
                start_date=today,
                end_date=today + relativedelta(months=duration),
                is_active=True
            )

    # Send success email
    send_mail(
        subject="Membership Purchase Successful",
        message=f"Dear {request.user.get_full_name() or request.user.username},\n\nYour membership for {plan.name} has been activated successfully.\nThank you for your purchase!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email],
        fail_silently=True,
    )

    return render(request, "payment_success.html")

# @csrf_exempt
# def membership_payment_success(request):
#     if not request.user.is_authenticated or request.user.is_cafe:
#         return HttpResponseForbidden("Cafés cannot complete membership payments.")
#     if request.method != "POST":
#         return HttpResponseBadRequest("Invalid request method.")

#     razorpay_payment_id = request.POST.get("razorpay_payment_id")
#     razorpay_order_id = request.POST.get("razorpay_order_id")
#     razorpay_signature = request.POST.get("razorpay_signature")
#     plan_id = request.POST.get("plan_id")

#     if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature, plan_id]):
#         return HttpResponseBadRequest("Missing payment data or plan ID")

#     try:
#         plan = MembershipPlan.objects.get(id=plan_id)
#     except MembershipPlan.DoesNotExist:
#         return HttpResponseBadRequest("Invalid membership plan selected.")

#     client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#     try:
#         client.utility.verify_payment_signature({
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_payment_id': razorpay_payment_id,
#             'razorpay_signature': razorpay_signature,
#         })
#         payment_status = 'success'
#     except SignatureVerificationError:
#         payment_status = 'failed'
#         PaymentRecord.objects.filter(order_id=razorpay_order_id).update(status='failed')
#         return render(request, "payment_failed.html")

#     payment_record, created = PaymentRecord.objects.get_or_create(
#         order_id=razorpay_order_id,
#         defaults={
#             'user': request.user,
#             'plan': plan,
#             'status': 'pending'
#         }
#     )
#     payment_record.payment_id = razorpay_payment_id
#     payment_record.signature = razorpay_signature
#     payment_record.status = payment_status
#     payment_record.save()

#     if payment_status != 'success':
#         return render(request, "payment_failed.html")

#     today = timezone.now().date()
#     active_membership = UserMembership.objects.filter(user=request.user, is_active=True).first()

#     if active_membership:
#         if active_membership.plan == plan:
#             base_date = max(active_membership.end_date, today) if active_membership.end_date else today
#             active_membership.end_date = base_date + relativedelta(months=1)
#             active_membership.save()
#         else:
#             active_membership.is_active = False
#             active_membership.save()
#             UserMembership.objects.create(
#                 user=request.user,
#                 plan=plan,
#                 start_date=today,
#                 end_date=today + relativedelta(months=1),
#                 is_active=True
#             )
#     else:
#         UserMembership.objects.create(
#             user=request.user,
#             plan=plan,
#             start_date=today,
#             end_date=today + relativedelta(months=1),
#             is_active=True
#         )

#     return render(request, "payment_success.html")