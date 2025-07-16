from django.db import models
from django.conf import settings

class Booking(models.Model):
    cafe = models.ForeignKey('cafe.Cafe', on_delete=models.CASCADE, related_name='bookings')  # Make sure 'cafe.Cafe' matches your cafe app/model name
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    people = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cafe.cafe_name} - {self.date} {self.time} ({self.people} people)"
