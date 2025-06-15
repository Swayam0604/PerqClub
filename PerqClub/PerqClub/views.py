from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request,'index.html')

def about_us(request):
    return render(request,'about-us.html')

def sign_up(request):
    form = UserCreationForm()
    return render(request,'sign-up.html',{'form':form})

def log_in(request):
    form = UserCreationForm()
    return render(request,'log-in.html',{'form':form})

