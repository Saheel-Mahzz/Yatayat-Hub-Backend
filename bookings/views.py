from django.shortcuts import render
from rest_framework import views
from rest_framework import viewsets

from bookings.models import Booking, BookingBusModel, Location, Trip
from bookings.serializers import BookingSerializer, LocationSerializer, TripReadSerializer, TripSerializer, TripWriteSerializer
from bookings.seriliazers import BusSerializer
from rest_framework.pagination import PageNumberPagination
# Create your views here.
class BusViewSets(viewsets.ModelViewSet):
    serializer_class = BusSerializer
    # why need to add pagination class??
    pagination_class = PageNumberPagination 
    def get_queryset(self):
        queryset= BookingBusModel.objects.all()
        # from_location = self.request.query_params.get('from_location')
        # to_location = self.request.query_params.get('to_location')
        passenger = self.request.query_params.get('passenger')
        # departure_time = self.request.query_params.get('departure_time')
        
        # if from_location:
        #     queryset = queryset.filter(from_location__icontains=from_location)
            
        # if to_location:
        #     queryset = queryset.filter(to_location__icontains=to_location)    
            
        if passenger:
            queryset = queryset.filter(available_seats__gte=int(passenger))    
            
        # if departure_time:
        #     queryset = queryset.filter(departure_time=departure_time)    
        return queryset    
    
class BookingViewSets(viewsets.ModelViewSet):    
    serializer_class = BookingSerializer
    def get_queryset(self):
        queryset = Booking.objects.all()
        trip_id = self.request.query_params.get('trip_id')
        if trip_id:
            queryset = queryset.filter(trip = trip_id)
        return queryset    
    
    
    
class LocationViewSets(viewsets.ModelViewSet):
    serializer_class= LocationSerializer
    queryset = Location.objects.all()    
class TripViewSets(viewsets.ModelViewSet):
    # queryset = Trip.objects.all()
    serializer_class = TripSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TripReadSerializer
        return TripWriteSerializer
    
    def get_queryset(self):
        queryset = Trip.objects.all()
        from_destination = self.request.query_params.get('from_location')
        to_destination = self.request.query_params.get('to_location')
        departure_time = self.request.query_params.get('departure_time')
        
        if from_destination:
            # queryset = queryset.filter(from_location__icontains= from_destination)
            queryset = queryset.filter(from_location=from_destination)
        if to_destination:
            queryset = queryset.filter(to_location = to_destination)
        if departure_time:
            queryset = queryset.filter(departure_time = departure_time)
        return queryset            
            