from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from cafe.models import Cafe, CafeLocation

from django.db.models import Q
def home(request):
    context ={
        'locations': CafeLocation.objects.all(),
    }
    return render(request,'index.html',context)

def about_us(request):
    context ={
        'locations': CafeLocation.objects.all(),
    }
    return render(request,'about-us.html',context)



def search(request):
    query = request.GET.get('q')
    if query:
        cafes = Cafe.objects.filter(cafe_name__icontains=query)

    else:
        cafes = Cafe.objects.all()
    
    locations = CafeLocation.objects.all()

    other_cafes = Cafe.objects.exclude(cafe_name__in=cafes.values_list('cafe_name', flat=True))

    return render(request, 'search.html', {'locations': locations, 'cafes': cafes, 'query': query,'other_cafes': other_cafes})


