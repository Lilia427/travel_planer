from django.contrib import admin
from .models import City, Event, Hotel, Transport, Order, Planner

# Реєстрація моделей у панелі адміністратора
admin.site.register(City)
admin.site.register(Event)
admin.site.register(Hotel)
admin.site.register(Transport)
admin.site.register(Order)
admin.site.register(Planner)
