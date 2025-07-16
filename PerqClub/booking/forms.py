from django import forms
from .models import Booking
from datetime import date, timedelta

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'people']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'booking-input'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'booking-input'}),
            'people': forms.NumberInput(attrs={'min': 1, 'max': 20, 'class': 'booking-input'}),
        }

    def clean_date(self):
        booking_date = self.cleaned_data.get('date')
        today = date.today()
        max_date = today + timedelta(days=7)
        if booking_date < today:
            raise forms.ValidationError("Booking for this date has already passed.")
        if booking_date > max_date:
            raise forms.ValidationError("You can only book up to 7 days in advance.")
        return booking_date