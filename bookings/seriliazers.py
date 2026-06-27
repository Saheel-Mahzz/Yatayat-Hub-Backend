
from rest_framework import serializers

from bookings.models import BookingBusModel

class BusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookingBusModel
        fields = "__all__"