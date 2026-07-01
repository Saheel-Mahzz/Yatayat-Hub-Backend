from rest_framework import serializers

from bookings.models import Booking, BookingBusModel, Location, Trip


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingBusModel
        fields = '__all__' # Yesle bus ko sabai parameters JSON banaundinchha

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__' # Yesle booking ko parameters handle garchha
        
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'          
        
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'        
        
class TripReadSerializer(serializers.ModelSerializer):
    bus = BusSerializer(read_only=True)  
    booked_seats = serializers.SerializerMethodField()
    class Meta:
        model = Trip
        fields = "__all__"       
    
    def get_booked_seats(self,obj):
        return Booking.objects.filter(trip=obj).values_list('seat_number',flat=True)    
        
class TripWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"        