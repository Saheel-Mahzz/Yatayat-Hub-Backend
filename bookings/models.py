from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class BookingBusModel(models.Model):
    name = models.CharField(max_length=50)
    total_seats = models.IntegerField(default=40)
    number_plate = models.CharField(max_length=200,unique=True)
    bus_type = models.CharField(max_length=50)

    # available_seats = models.IntegerField(default=40)
    total_seats = models.IntegerField(default=40)
    
    def __str__(self):
        return f'{self.name} ({self.number_plate})'
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.name}'    
    
            
class Trip(models.Model):
    # from_location = models.CharField(max_length=200)
    # to_location = models.CharField(max_length=200)
    
    from_location = models.ForeignKey(Location,on_delete=models.CASCADE,related_name='deprating_trips')
    to_location = models.ForeignKey(Location,on_delete=models.CASCADE,related_name='arriving_trips')
    departure_time = models.DateField()
    
    bus = models.ForeignKey(BookingBusModel,on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()   
    available_seats = models.IntegerField(null=True,blank=True)
    # price = models.DecimalField(max_digits=7,decimal_places=5,default=0.00)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    
    def save(self, *args, **kwargs):
        # if not self.available_seats:
        if self.available_seats is None:
            self.available_seats = self.bus.total_seats
        super().save(*args,**kwargs)
         
    
    def __str__(self):
        return f'{self.route} on {self.date}'
    
class Booking(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True, blank=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=40)
    booked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('trip','seat_number')    
        
    def __str__(self):
        return f'{self.user.username} - {self.trip} - {self.seat_number}'    
    
