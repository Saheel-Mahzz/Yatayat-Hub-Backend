from django.shortcuts import render
from rest_framework import views
from rest_framework import viewsets

from bookings.models import BookingBusModel
from bookings.seriliazers import BusSerializer
# Create your views here.
class BusViewSets(viewsets.ModelViewSet):
    serializer_class = BusSerializer
    
    def get_queryset(self):
        queryset= BookingBusModel.objects.all()
        from_location = self.request.query_params.get('from_location')
        to_location = self.request.query_params.get('to_location')
        passenger = self.request.query_params.get('passenger')
        departure_time = self.request.query_params.get('departure_time')
        
        if from_location:
            queryset = queryset.filter(from_location__icontains=from_location)
            
        if to_location:
            queryset = queryset.filter(to_location__icontains=to_location)    
            
        if passenger:
            queryset = queryset.filter(available_seats__gte=int(passenger))    
            
        if departure_time:
            queryset = queryset.filter(departure_time=departure_time)    
        return queryset    