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
    return render(request, 'bookings-list.html', {'bookings': bookings})
