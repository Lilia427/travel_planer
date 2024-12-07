from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return self.name

class Hotel(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    distance_to_center = models.FloatField()
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Transport(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=[
        ('train', 'Потяг'),
        ('bus', 'Автобус'),
        ('own', 'Власний транспорт'),
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        if self.type == 'own':
            return "Власний транспорт"
        return f"{self.type} ({self.city.name})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    transport = models.ForeignKey(Transport, on_delete=models.SET_NULL, null=True, blank=True)
    events = models.ManyToManyField(Event, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        total = 0
        if self.hotel:
            total += self.hotel.price_per_night
        if self.transport and self.transport.type != 'own':
            total += self.transport.price
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class Planner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    events = models.ManyToManyField(Event)

    def __str__(self):
        return f"Planner for {self.user.username}"
