from django.urls import path
from . import views
from .views import CafeDetailWithReviewsView, AllReviewsListView

urlpatterns = [
    path('', views.cafe, name='cafe_list'),
    # path('<int:pk>/', views.cafe_detail_view, name='cafe_detail'),
    # path('reviews',views.cafereview,name='reviews'),

    # UPDATED: This path now points to your CafeDetailWithReviewsView.
    # It will serve as the main detail page for a cafe, including initial reviews and the submission form.
    # The 'pk' from the URL will be automatically passed as 'cafe_id' to CafeDetailWithReviewsView.
    path('<int:pk>/', CafeDetailWithReviewsView.as_view(), name='cafe_detail'),

    # NEW: Path to show ALL reviews specifically for a particular cafe.
    # This will be triggered when "See All Reviews" is clicked from a cafe's detail page.
    # The 'pk' from the URL will be passed as 'cafe_id' to AllReviewsListView.
    path('<int:pk>/cafe-reviews/', AllReviewsListView.as_view(), name='cafe_reviews'),
    path('<slug:slug>',views.CafeLocationDetails.as_view(),name='cafe_location')
]
