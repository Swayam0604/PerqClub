from django.contrib import admin
from .models import Booking
from datetime import time
# Register your models here.


class TimeSlotFilter(admin.SimpleListFilter):
    title = 'Time of Day'
    parameter_name = 'time_slot'

    def lookups(self, request, model_admin):
        return [
            ('morning', 'Morning (6 AM - 12 PM)'),
            ('afternoon', 'Afternoon (12 PM - 5 PM)'),
            ('evening', 'Evening (5 PM - 9 PM)'),
            ('night', 'Night (9 PM - 6 AM)'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'morning':
            return queryset.filter(time__gte=time(6, 0), time__lt=time(12, 0))
        elif value == 'afternoon':
            return queryset.filter(time__gte=time(12, 0), time__lt=time(17, 0))
        elif value == 'evening':
            return queryset.filter(time__gte=time(17, 0), time__lt=time(21, 0))
        elif value == 'night':
            return queryset.filter(time__gte=time(21, 0)) | queryset.filter(time__lt=time(6, 0))
        return queryset

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['cafe', 'user', 'date', 'formatted_time', 'people', 'created_at']
    list_filter = ['cafe', 'date', TimeSlotFilter]  # ⬅️ Add the custom filter here

    def formatted_time(self, obj):
        return obj.time.strftime('%I:%M %p')
    formatted_time.short_description = 'Time'


