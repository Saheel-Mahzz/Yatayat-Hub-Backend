from django.shortcuts import render
from rest_framework import views
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from bookings.models import Booking, BookingBusModel, Location, Trip
from bookings.serializers import BookingSerializer, BookingWriteSerializer, LocationSerializer, TripReadSerializer, TripSerializer, TripWriteSerializer
from bookings.seriliazers import BusSerializer
from rest_framework.pagination import PageNumberPagination
from .utils import generate_ticket_pdf
from rest_framework.decorators import action
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
    permission_classes=[IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookingSerializer
        return BookingWriteSerializer
    
    def create(self, request, *args, **kwargs):
        # Request bata aako data (user, trip, seat) lai Write Serializer maa pathaune
        serializer = self.get_serializer_class()(data=request.data)
        
        # Validation check garne (kunai seat khali chaina bhane error faldinchha)
        serializer.is_valid(raise_exception=True)
        booking_instance = serializer.save(user=self.request.user)
        
        # Database maa record save garne ani tyo naya niko booking object (instance) line
        # booking_instance = serializer.save()
        
        # --- LOGIC GATES YAHA HO ---
        
        current_trip = booking_instance.trip
        print(f"BEFORE MINUS: {current_trip.available_seats}")
        current_trip.available_seats -= 1
        current_trip.save()
        print(f"AFTER MINUS: {current_trip.available_seats}")
        # Aba response return garda, write serializer hoina, detailed version use garne!
        response_serializer = BookingSerializer(booking_instance)
        
        # Success status (201 Created) ko sathai full detailed data return gardi ne
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    def get_queryset(self):
        # queryset = Booking.objects.all()
        queryset = Booking.objects.filter(user=self.request.user)
        trip_id = self.request.query_params.get('trip_id')
        if trip_id:
            queryset = queryset.filter(trip = trip_id)
        return queryset    
    @action(detail=True, methods=['get'], url_path='download')
    def download_pdf(self, request, pk=None):
        booking = self.get_object() # 1. Object line
        
        response = generate_ticket_pdf(booking) # 2. Helper lai call garne
        
        if response:
            return response # 3. PDF return garne
            
        return Response({'error': 'PDF render error'}, status=400)
    
    
class LocationViewSets(viewsets.ModelViewSet):
    serializer_class= LocationSerializer
    queryset = Location.objects.all()    
    pagination_class=None
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
          
            