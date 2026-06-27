from django.db import models

# Create your models here.
class BookingBusModel(models.Model):
    name = models.CharField(max_length=50)
    total_seats = models.IntegerField()
    number_plate = models.IntegerField()
    bus_type = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.name} ({self.number_plate})'
    
    
        