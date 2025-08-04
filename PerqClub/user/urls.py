from django.urls import path
from . import views


urlpatterns = [
    path('sign-up/', views.register_view, name='register_user'),
    path('verify/', views.verify_otp_view, name='verify-otp'),
    path('login/', views.login_view, name='login_user'),
    path('logout/', views.logout_view, name='logout_user'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact_view, name='contact'),
    path('edit-cafe/', views.edit_cafe, name='edit_cafe'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/',views.change_password,name='change_password')
]
