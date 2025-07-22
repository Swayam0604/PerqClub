from django.urls import path
from . import views

urlpatterns = [
    path('',views.membership_plans_view,name="membership"),
    # path('subscribe/<int:plan_id>/', views.subscribe_to_plan, name='subscribe_to_plan'),
    # path('payment_success/', views.payment_success_view, name='payment_success'),
    path('checkout/', views.checkout_view, name='membership_checkout'),
    path('payment/success/', views.membership_payment_success, name='membership_payment_success'),
]
