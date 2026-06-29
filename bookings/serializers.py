from rest_framework import serializers

from bookings.models import Booking, BookingBusModel, Trip


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingBusModel
        fields = '__all__' # Yesle bus ko sabai parameters JSON banaundinchha

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__' # Yesle booking ko parameters handle garchha
        
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'        