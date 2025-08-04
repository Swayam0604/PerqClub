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
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from booking.models import Booking
from cafe.models import CafeReview, Cafe
from membership.models import UserMembership
from django.contrib.auth import get_user_model
from .forms import UserProfileForm


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cafe.models import Cafe, CafeReview
from booking.models import Booking
from user.models import CustomUser





@login_required
def profile(request):
    user = request.user

    # Count user-specific data
    bookings_count = Booking.objects.filter(user=user).count()
    reviews_count = CafeReview.objects.filter(user=user).count()

    context = {
        'bookings_count': bookings_count,
        'reviews_count': reviews_count,
        'membership': None,  # Placeholder in case template still references it
    }

    # For superuser: Admin stats
    if user.is_superuser:
        context.update({
            'cafes_count': Cafe.objects.count(),
            'user_count': CustomUser.objects.count(),
            'memberships_count': 0,  # No membership model, so set to 0
            'all_cafes': Cafe.objects.all(),
        })

    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('edit_profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed.")
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .forms import ContactForm
from .models import ContactMessage

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Save message to database
            ContactMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=data['name'],
                email=data['email'],
                subject=data['subject'],
                message=data['message'],
            )

            # Send email to admin
            subject = f"New Contact Form Submission: {data['subject']}"
            message = (
                f"Name: {data['name']}\n"
                f"Email: {data['email']}\n"
                f"Subject: {data['subject']}\n"
                f"Message:\n{data['message']}\n"
                f"Submitted by: {request.user.username if request.user.is_authenticated else 'Anonymous'}"
            )
            admin_email = settings.DEFAULT_FROM_EMAIL
            send_mail(subject, message, data['email'], [admin_email])

            # Show success message and redirect
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')

    else:
        if request.user.is_authenticated:
            initial_data = {
                'name': request.user.get_full_name(),
                'email': request.user.email,
            }
            form = ContactForm(initial=initial_data)
            form.fields['name'].widget.attrs['readonly'] = True
            form.fields['email'].widget.attrs['readonly'] = True
        else:
            form = ContactForm()

    return render(request, 'contact.html', {'form': form})

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout
# from django.shortcuts import render, redirect

# @login_required
# def delete_user(request):
#     if request.method == "POST":
#         user = request.user
#         user.delete()  # Delete the user
#         logout(request)  # Log out after deletion
#         return redirect("login")  # Redirect to login page

#     # On GET, show confirmation page
#     return render(request, "accounts/delete_confirm.html")

# views.py

from cafe.forms import CafeForm, CafeImageFormSet, CafeHighlightFormSet, AdminCafeForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
# Add these imports at the top of your views.py file
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cafe.forms import CafeForm, CafeImageFormSet, CafeHighlightFormSet, AdminCafeForm
from cafe.models import Cafe

@login_required
def edit_cafe(request):
    print(">>> edit_cafe view triggered")

    # 1) Which cafes can this user see?
    if request.user.is_superuser:
        all_cafes = Cafe.objects.all()
    else:
        all_cafes = request.user.cafes.all()

    # 2) Grab the GET parameter
    cafe_id = request.GET.get('cafe_id')
    print(f">>> Received cafe_id: {cafe_id}")

    # 2a) If user clicked "+ Add New Café" in the dropdown:
    if cafe_id == 'add':
        print(">>> Redirecting to register_cafe")
        return redirect('register_cafe')

    # 3) If they picked a real cafe_id, load it (or 404)
    cafe = None
    if cafe_id:
        try:
            cafe = get_object_or_404(Cafe, pk=cafe_id)
            print(f">>> Found cafe: {cafe.cafe_name}")
            # permission check
            if not request.user.is_superuser and cafe not in all_cafes:
                messages.error(request, "You don't have permission to edit this cafe.")
                return redirect('edit_cafe')  # Redirect back to edit_cafe instead of permission_denied
        except Exception as e:
            print(f">>> Error finding cafe: {e}")
            messages.error(request, "Cafe not found.")
            return redirect('edit_cafe')

    # 4) If no cafe chosen yet, show only the selector dropdown
    if not cafe:
        print(">>> No cafe selected, showing dropdown only")
        return render(request, 'edit_cafe.html', {
            'all_cafes': all_cafes,
            'cafe': None,
        })

    # 5) Decide which form class for details
    FormClass = CafeForm if request.user.is_superuser else CafeForm

    # 6) Handle POST vs GET
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        print(f">>> POST form_type: {form_type}")

        cafe_form = FormClass(request.POST, instance=cafe)
        image_formset = CafeImageFormSet(
            request.POST, request.FILES,
            instance=cafe,
            prefix='images',
            form_kwargs={'image_required': False}
        )
        highlight_formset = CafeHighlightFormSet(
            request.POST, instance=cafe,
            prefix='highlights'
        )

        # 6a) Update only café details
        if form_type == 'cafe':
            if cafe_form.is_valid():
                cafe_form.save()
                messages.success(request, "Cafe details updated.")
                return redirect(f"{reverse('edit_cafe')}?cafe_id={cafe.id}")
            else:
                print("Cafe form errors:", cafe_form.errors)
                messages.error(request, "Please correct the errors in cafe details.")

        # 6b) Update only images
        elif form_type == 'images':
            if image_formset.is_valid():
                image_formset.save()
                messages.success(request, "Cafe images updated.")
                return redirect(f"{reverse('edit_cafe')}?cafe_id={cafe.id}")
            else:
                print("Image formset errors:", image_formset.errors)
                messages.error(request, "Please correct the errors in cafe images.")

        # 6c) Update only highlights
        elif form_type == 'highlights':
            if highlight_formset.is_valid():
                highlight_formset.save()
                messages.success(request, "Cafe highlights updated.")
                return redirect(f"{reverse('edit_cafe')}?cafe_id={cafe.id}")
            else:
                print("Highlight formset errors:", highlight_formset.errors)
                messages.error(request, "Please correct the errors in cafe highlights.")

    else:
        # 7) GET: instantiate unbound forms/formsets
        cafe_form = FormClass(instance=cafe)
        image_formset = CafeImageFormSet(
            instance=cafe,
            prefix='images',
            form_kwargs={'image_required': False}
        )
        highlight_formset = CafeHighlightFormSet(
            instance=cafe,
            prefix='highlights'
        )

    # 8) Render everything
    print(f">>> Rendering template with cafe: {cafe.cafe_name if cafe else 'None'}")
    return render(request, 'edit_cafe.html', {
        'all_cafes': all_cafes,
        'cafe': cafe,
        'cafe_form': cafe_form,
        'image_formset': image_formset,
        'highlight_formset': highlight_formset,
    })