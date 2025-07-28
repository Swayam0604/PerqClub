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
