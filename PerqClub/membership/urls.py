from django.urls import path
from . import views

urlpatterns = [
    path('',views.membership_plans_view,name="membership"),
    # path('subscribe/<int:plan_id>/', views.subscribe_to_plan, name='subscribe_to_plan'),
    path('payment_success/', views.payment_success_view, name='payment_success'),
]
