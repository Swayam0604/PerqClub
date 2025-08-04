from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from cafe.models import Cafe  # adjust if your cafe app is named differently
from django.contrib.auth.decorators import login_required

def create_booking(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.cafe = cafe
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            messages.success(request, "Table booked successfully!")
            return redirect('cafe_detail', pk=cafe.id)
    else:
        form = BookingForm()
    return render(request, 'cafe-details.html', {'form': form, 'cafe': cafe})

def cafe_bookings(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    bookings = cafe.bookings.order_by('-date', '-time')
    return render(request, 'bookings-list.html', {'cafe': cafe, 'bookings': bookings})

@login_required
def booking_list(request):
    if request.user.is_staff or request.user.is_superuser:
        # Show all bookings, or filter by cafe if needed
        bookings = Booking.objects.all().order_by('-date', '-time')
    else:
        bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
    cafe = bookings.first().cafe if bookings.exists() else None
    return render(request, 'bookings-list.html', {'bookings': bookings,'cafe': cafe})

from django.core.mail import send_mail
from django.conf import settings  # to get DEFAULT_FROM_EMAIL
from django.contrib.auth.decorators import user_passes_test, login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
@login_required
def update_booking_status(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)
        status = request.POST.get('status')

        if status in ['accepted', 'rejected']:
            booking.status = status
            booking.save()
            messages.success(request, f'Booking marked as {status}.')

            # Send email notification
            subject = f"Your booking has been {status}"
            message = (
                f"Hello {booking.user.first_name or booking.user.username},\n\n"
                f"Your booking at '{booking.cafe.cafe_name}' on {booking.date} at {booking.time.strftime('%I:%M %p')} "
                f"has been {status.upper()}.\n\n"
                "Thank you for using our service.\n\n"
                "Best regards,\nCafe Team"
            )
            recipient_list = [booking.user.email]
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        else:
            messages.error(request, 'Invalid status value.')

    return redirect('booking_list')
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking

@login_required
@require_POST
def user_cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status in ['pending', 'accepted']:
        booking.status = 'cancelled'
        booking.save()
        
        # Email to the user
        user_subject = f"Booking Cancelled for {booking.cafe.cafe_name}"
        user_message = (
            f"Hello {booking.user.first_name or booking.user.username},\n\n"
            f"Your booking at '{booking.cafe.cafe_name}' on {booking.date} at {booking.time.strftime('%I:%M %p')} "
            "has been cancelled as per your request.\n\n"
            "Best regards,\nPerqClub Team"
        )

        try:
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [booking.user.email]
            )
            messages.success(request, "Your booking has been cancelled and a confirmation email has been sent to you.")
        except Exception as e:
            messages.warning(request, "Booking cancelled, but an error occurred while sending the confirmation email.")

    else:
        messages.warning(request, "This booking cannot be cancelled.")

    return redirect('booking_list')
