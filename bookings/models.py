from django.db import models

# Create your models here.
class BookingBusModel(models.Model):
    name = models.CharField(max_length=50)
    total_seats = models.IntegerField(default=40)
    number_plate = models.IntegerField()
    bus_type = models.CharField(max_length=50)
    from_location = models.CharField(max_length=200)
    to_location = models.CharField(max_length=200)
    departure_time = models.DateField()
    available_seats = models.IntegerField(default=40)
    
    def __str__(self):
        return f'{self.name} ({self.number_plate})'
    
    
        