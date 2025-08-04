from booking.models import Booking
from cafe.models import Cafe, CafeReview
from user.models import CustomUser
from membership.models import UserMembership

def user_stats(request):
    if request.user.is_authenticated:
        user = request.user

        # ✅ Case 1: Superuser
        if user.is_superuser:
            # Count memberships for superuser
            try:
                memberships_count = UserMembership.objects.filter(is_active=True).count()
            except:
                try:
                    memberships_count = UserMembership.objects.count()
                except:
                    memberships_count = 0

            return {
                'bookings_count': Booking.objects.count(),
                'reviews_count': CafeReview.objects.count(),
                'user_count': CustomUser.objects.count(),
                'cafes_count': Cafe.objects.count(),
                'memberships_count': memberships_count,
            }

        # ✅ Case 2: Cafe manager
        cafes = Cafe.objects.filter(manager=user)
        if cafes.exists():
            return {
                'bookings_count': Booking.objects.filter(cafe__in=cafes).count(),
                'reviews_count': CafeReview.objects.filter(cafe__in=cafes).count(),
            }

        # ✅ Case 3: Normal User - Provide full membership object
        try:
            user_membership = UserMembership.objects.select_related('plan').get(user=user)
            membership = user_membership
            membership_status = "Active" if user_membership.is_active else "Inactive"
        except UserMembership.DoesNotExist:
            membership = None
            membership_status = "No Membership"
        
        return {
            'bookings_count': Booking.objects.filter(user=user).count(),
            'reviews_count': CafeReview.objects.filter(user=user).count(),
            'membership': membership,  # Full membership object
            'membership_status': membership_status,  # String status
        }

    return {}


from cafe.models import Cafe

def admin_cafes(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return {'all_cafes': Cafe.objects.all()}
    return {}