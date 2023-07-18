
from django.contrib import admin
from django.db import models
from .models import CarType, Vehicle, Buyer, OrderVehicle, Description, LabMember

# Register your models here.
admin.site.register(CarType)
admin.site.register(Vehicle)
admin.site.register(Buyer)
admin.site.register(OrderVehicle)
admin.site.register(Description)
admin.site.register(LabMember)

