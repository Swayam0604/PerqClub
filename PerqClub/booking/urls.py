from django.urls import path
from . import views

urlpatterns = [
    path('cafe/<int:cafe_id>/book/', views.create_booking, name='create_booking'),
    path('cafe/<int:cafe_id>/bookings/', views.cafe_bookings, name='cafe_bookings'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('booking/<int:booking_id>/update-status/', views.update_booking_status, name='update_booking_status'),
    path('booking/<int:booking_id>/cancel/', views.user_cancel_booking, name='user_cancel_booking'),

]
