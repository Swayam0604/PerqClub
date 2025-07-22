from django.shortcuts import render, get_object_or_404, redirect
from .models import MembershipPlan
# from django.contrib.auth.decorators import login_required
from django.utils import timezone
from cafe.models import CafeLocation
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import MembershipPlan  # or whatever your model is called
from .models import MembershipPlan, UserMembership
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from razorpay.errors import SignatureVerificationError

def membership_plans_view(request):
    plans = MembershipPlan.objects.all().prefetch_related('features')
    context= {
        'plans': plans,
        'locations': CafeLocation.objects.all()
    }
    return render(request, 'membership.html', context)




def checkout_view(request):
    membership_id = request.GET.get('membership_id') or request.POST.get('membership_id')
    if membership_id:
        membership = MembershipPlan.objects.get(id=membership_id)
    else:
        # Fallback: show the first plan or handle error
        membership = MembershipPlan.objects.first()
    # Now you can safely use membership.price
    amount = int(membership.price * 100)

    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    data = { "amount": amount, "currency": "INR", "receipt": f"membership_{request.user.id}_{membership.id}" }
    # data1 = { "amount": 900000, "currency": "INR", "receipt": f"membership12_{request.user.id}_{membership.id}" }

    payment_details = client.order.create(data=data)

    # payment_detailss = client.order.create(data=data1)

    context = {
        'memberships': MembershipPlan.objects.all(), # Keep this for context, but not used in the new_code
        'current_membership': UserMembership.objects.get(user=request.user, is_active=True).plan if UserMembership.objects.filter(user=request.user).exists() else None, # Keep this for context
        'is_upgrade': False, # Keep this for context
        'memberships_json': json.dumps([
            {
                'id': m.id,
                'name': m.name,
                'description': m.description,
                'price': m.price,
                'perks': [str(feature.feature_text) for feature in m.features.all()],
            }
            for m in MembershipPlan.objects.all()
        ], cls=DjangoJSONEncoder), # Keep this for context
        "payment_details": payment_details,
        # "payment_detailss": payment_detailss,

    }
    return render(request, 'checkout.html', context)

@csrf_exempt
def membership_payment_success(request):
    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
        # Mark membership as active for the user here
        # Send confirmation email if needed
        return render(request, "payment_success.html")
    except SignatureVerificationError:
        return render(request, "payment_failed.html")