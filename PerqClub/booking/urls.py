from django.urls import path
from . import views

urlpatterns = [
    path('cafe/<int:cafe_id>/book/', views.create_booking, name='create_booking'),
    path('cafe/<int:cafe_id>/bookings/', views.cafe_bookings, name='cafe_bookings'),
    path('bookings/', views.booking_list, name='booking_list'),
]
