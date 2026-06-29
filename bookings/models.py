from django.db import models
from django.contrib.auth.models import User
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
    
    
class Trip(models.Model):
    route = models.CharField(max_length=200)
    bus= models.ForeignKey(BookingBusModel,on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()    
    
    def __str__(self):
        return f'{self.route} on {self.date}'
    
class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=40)
    booked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('trip','seat_number')    
        
    def __str__(self):
        return f'{self.user.username} - {self.trip} - {self.seat_number}'    
    
        