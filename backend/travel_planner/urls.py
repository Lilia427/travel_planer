"""
URL configuration for travel_planner project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Адмінка
    path('', include('trips.urls')),  # Підключення маршрутів додатка trips
]
