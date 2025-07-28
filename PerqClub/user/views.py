from django.shortcuts import render
import random
from django.contrib.auth import get_user_model
# Create your views here.

from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import OTP, CustomUser
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from booking.models import Booking  # adjust import as per your app
from cafe.models import CafeReview, Cafe   # adjust import as per your app
from membership.models import UserMembership

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = "Perqclub Email Verification - OTP"
    message = f"Your OTP for Perqclub registration is: {otp}.\nPlease enter this code to complete your registration.\nThank you for choosing Perqclub."
    from_email = None  # Uses DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            user_data['is_cafe'] = request.POST.get('is_cafe') == 'on'  # Check if checkbox is checked
            request.session['user_data'] = form.cleaned_data
            otp_code = generate_otp()
            request.session['otp_code'] = otp_code

            # Save OTP to database
            OTP.objects.create(
                phone_number=form.cleaned_data['phone_number'],
                otp_code=otp_code
            )

            # Send OTP to email
            send_otp_email(form.cleaned_data['email'], otp_code)

            return redirect('verify-otp')
    else:
        form = RegistrationForm()
    return render(request, 'sign-up.html', {'form': form})


def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        otp_code = request.session.get('otp_code')
        user_data = request.session.get('user_data')
        if entered_otp == otp_code and user_data:
            # Create and save the user
            User = get_user_model()
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                # Use .get() for optional fields
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', ''),
                phone_number=user_data['phone_number'],
                is_active=True,
                is_staff=user_data.get('is_cafe', False)  # Set is_staff if is_cafe is true
            )
            user.set_password(user_data['password1'])  # or 'password'
            user.save()
            print(f"User created successfully: {user.username}, Email: {user.email}, Phone: {user.phone_number}")
            messages.success(request, "Account created and verified!")
            # Optionally, clear session data
            request.session.pop('user_data', None)
            request.session.pop('otp_code', None)
            return redirect('login_user')
        else:
            print(f"OTP verification failed. Entered: {entered_otp}, Expected: {otp_code}")
            messages.error(request, "Invalid or expired OTP.")
    return render(request, 'verify-otp.html')


from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from membership.models import UserMembership
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    next_url = request.GET.get('next', 'home')  # Default redirect if no next is given
    reason = request.GET.get('reason')  # New: capture reason for login prompt

    if request.method == 'GET':
        # Show appropriate message based on `reason` or `next` URL
        if reason == 'booking':
            messages.error(request, "You need to login to reserve a table.")
        elif reason == 'review':
            messages.error(request, "You must be logged in to write a review.")
        elif next_url == '/membership/':
            messages.error(request, "You need to login to access the membership page.")
        elif next_url == '/checkout/':
            messages.error(request, "Login required to proceed to checkout.")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.POST.get('next', next_url))  # Preserve redirection
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'log-in.html', {'next': next_url})




def logout_view(request):
    """
    Logout view that logs out the user and redirects to login page
    """
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login_user')

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.shortcuts import render, redirect
from .forms import UserProfileForm
from booking.models import Booking
from cafe.models import CafeReview
from membership.models import UserMembership
from cafe.models import Cafe

User = get_user_model()

@login_required
def profile(request):
    user = request.user
    membership = UserMembership.objects.filter(user=user).order_by('-is_active', '-end_date').first()

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)

        if profile_form.is_valid() and (not request.POST.get('old_password') or password_form.is_valid()):
            profile_form.save()

            if request.POST.get('old_password'):
                user = password_form.save()
                update_session_auth_hash(request, user)

            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user)
        password_form = PasswordChangeForm(user)

    # Stats based on role
    if user.is_superuser:
        bookings_count = Booking.objects.count()
        reviews_count = CafeReview.objects.count()
        memberships_count = UserMembership.objects.count()
        cafes_count = Cafe.objects.count()
        user_count = User.objects.count()
    elif user.is_cafe:
        cafes = Cafe.objects.filter(manager=user)
        bookings_count = Booking.objects.filter(cafe__in=cafes).count()
        reviews_count = CafeReview.objects.filter(cafe__in=cafes).count()
        memberships_count = 0
        cafes_count = cafes.count()
        user_count = None
    else:
        bookings_count = Booking.objects.filter(user=user).count()
        reviews_count = CafeReview.objects.filter(user=user).count()
        memberships_count = UserMembership.objects.filter(user=user).count()
        cafes_count = 0
        user_count = None

    return render(request, 'profile.html', {
        'form': profile_form,
        'password_form': password_form,
        'membership': membership,
        'bookings_count': bookings_count,
        'reviews_count': reviews_count,
        'memberships_count': memberships_count,
        'cafes_count': cafes_count,
        'user_count': user_count,
    })
