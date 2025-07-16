from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.register_view, name='register_user'),
    path('verify/', views.verify_otp_view, name='verify-otp'),
    path('login/', views.login_view, name='login_user'),
    path('logout/', views.logout_view, name='logout_user'),
]
