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

def generate_otp():
    return str(random.randint(100000, 999999))

# def send_otp_textbelt(phone_number, otp):
#     response = requests.post('https://textbelt.com/text', {
#         'phone': phone_number,
#         'message': f'Your OTP for Registration Perqclub is: {otp}',
#         'key': 'textbelt'  # Free key: allows 1 SMS/day
#     })
#     return response.json()

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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'log-in.html')  # Render the login template
    else:
        return render(request, 'log-in.html')  # Render the login template


def logout_view(request):
    """
    Logout view that logs out the user and redirects to login page
    """
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login_user')



