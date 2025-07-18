"""
URL configuration for PerqClub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from PerqClub import views as main_views  # home, about_us, etc.
from django.conf import settings
from django.conf.urls.static import static
from cafe import views as cafe_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',main_views.home,name="home"),
    path('about-us',main_views.about_us,name="About-us"),
    path('cafes/', include('cafe.urls'),name="Cafes"), 
    path("user",include("user.urls"), name="register"),
    path('register-cafe',cafe_views.register_cafe_view,name="register_cafe"),
    path('registration-success/', cafe_views.registration_success_view, name='registration_success'),
    path('search/', main_views.search, name='search'),
    path('membership/',include('membership.urls'),name="membership"),
    path('booking/', include('booking.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)