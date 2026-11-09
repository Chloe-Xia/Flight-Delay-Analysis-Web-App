"""
URL configuration for book project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from users import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('',include('users.urls')), #Transfer to App Users
    path('', views.login),
    path('login/', views.login),
    path('index/', views.index),
    path('register/', views.register),
    path('search/', views.search),
    path('analysis/', views.analysis),
    path('comment/', views.comment),
    path('ranking/', views.ranking),
    path('favorite_d/', views.favorite_d),
    path('search_flight/', views.search_flight, name='search'),
    path('favorite/', views.favorite, name='favorite'),
    path('add_to_favorite/', views.add_to_favorite, name='add_to_favorite'),
    path('remove_from_favorite/', views.remove_from_favorite, name='remove_from_favorite'),
    path('weather/<str:city_name>/', views.get_city_weather, name='get_city_weather'),
]