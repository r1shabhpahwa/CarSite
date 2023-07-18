from django.db import models
from django.contrib.auth.models import User


# Car type with the fields length being determined below
class CarType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


# Vehicles model
class Vehicle(models.Model):
    cartype = models.ForeignKey(CarType, related_name='vehicles', on_delete=models.CASCADE)
    car_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=6)
    inventory = models.PositiveIntegerField(default=10)
    instock = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    # New field for car features
    cruise_control = models.BooleanField(default=False)
    audio_interface = models.BooleanField(default=False)
    airbags = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    seat_heating = models.BooleanField(default=False)
    park_assist = models.BooleanField(default=False)
    power_steering = models.BooleanField(default=False)
    reversing_camera = models.BooleanField(default=False)
    auto_start_stop = models.BooleanField(default=False)

    def __str__(self):
        return self.car_name


# Buyer Model
class Buyer(User):
    AREA_CHOICES = [
        ('C', 'Chatham'),
        ('LS', 'LaSalle'),
        ('A', 'Amherstburg'),
        ('W', 'Windsor'),
        ('L', 'Lakeshore'),
        ('T', 'Toronto'),
        ('WA', 'Waterloo'),
        ('LE', 'Leamington'),
    ]
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    area = models.CharField(max_length=2, choices=AREA_CHOICES, default='C')
    interested_in = models.ManyToManyField(CarType)

    def __str__(self):
        return self.username


# OrderVehicle model
class OrderVehicle(models.Model):
    STATUS_CHOICES = [
        (0, 'Cancelled'),
        (1, 'Placed'),
        (2, 'Shipped'),
        (3, 'Delivered'),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    vehicles_ordered = models.PositiveIntegerField()
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1)
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"Order ID: {self.pk}"

    def total_price(self):
        return self.vehicle.price * self.vehicles_ordered


class Description(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LabMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    semester = models.IntegerField()
    personal_page = models.URLField()

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['first_name']
