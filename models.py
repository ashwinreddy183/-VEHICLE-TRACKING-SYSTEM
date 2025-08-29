from django.db import models

# Create your models here.

class BusInfo(models.Model):
    bus_number = models.CharField(max_length=20)
    seating_capacity = models.PositiveIntegerField()
    longitude = models.DecimalField(max_digits=19, decimal_places=15)
    latitude = models.DecimalField(max_digits=19, decimal_places=15)
    starting_point = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    is_running = models.BooleanField(default=False)  # New field

    def __str__(self):
        return self.bus_number
    
from django.db import models

class AutorickshawInfo(models.Model):
    vehicle_number = models.CharField(max_length=20)
    driver_name = models.CharField(max_length=255)
    is_running = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=20)
    longitude = models.DecimalField(max_digits=19, decimal_places=15)
    latitude = models.DecimalField(max_digits=19, decimal_places=15)
    pending_bookings_count = models.PositiveIntegerField(default=0)
    vehicle_key = models.CharField(max_length=15,)

    def __str__(self):
        return self.vehicle_number








 