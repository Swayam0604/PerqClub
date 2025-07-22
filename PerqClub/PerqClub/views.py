from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from cafe.models import Cafe, CafeLocation

from django.db.models import Q
def home(request):
    # Fetch approved cafes that are marked as "Cafe of the Week"
    cafes_of_the_week = Cafe.objects.filter(is_cafe_of_the_week=True, is_approved=True)[:6]
    
    # Also fetch locations to populate the dropdown in the navbar
    locations = CafeLocation.objects.all()

    context = {
        'cafes_of_the_week': cafes_of_the_week,
        'locations': locations,
    }
    return render(request, 'index.html', context)

def about_us(request):
    # This context is needed for the navbar location dropdown
    context = {'locations': CafeLocation.objects.all()}
    return render(request, 'about-us.html', context)



def search(request):
    # This context is needed for the navbar location dropdown
    query = request.GET.get('q', '')
    cafes = Cafe.objects.filter(cafe_name__icontains=query, is_approved=True)
    context = {
        'cafes': cafes,
        'query': query,
        'locations': CafeLocation.objects.all(),
    }
    return render(request, 'search.html', context)


