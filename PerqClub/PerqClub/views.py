from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from cafe.models import Cafe, CafeLocation

def home(request):
    return render(request,'index.html',{'locations': CafeLocation.objects.all()})

def about_us(request):
    return render(request,'about-us.html',{'locations': CafeLocation.objects.all()})

def sign_up(request):
    form = UserCreationForm()
    return render(request,'sign-up.html',{'form':form,'locations': CafeLocation.objects.all()})

def log_in(request):
    form = UserCreationForm()
    return render(request,'log-in.html',{'form':form})

def search(request):
    query = request.GET.get('q')
    if query:
        locations = CafeLocation.objects.filter(location_name__icontains=query)
        if not locations:
            cafes = Cafe.objects.filter(cafe_name__icontains=query)
        else:
            cafes = Cafe.objects.all()
    else:
        locations = CafeLocation.objects.all()
    return render(request, 'search.html', {'locations': locations, 'cafes': cafes, 'query': query})

