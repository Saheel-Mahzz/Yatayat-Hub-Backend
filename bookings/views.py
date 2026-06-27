from django.shortcuts import render
from rest_framework import views
from rest_framework import viewsets

from bookings.models import BookingBusModel
from bookings.seriliazers import BusSerializer
# Create your views here.
class BusViewSets(viewsets.ModelViewSet):
    queryset= BookingBusModel.objects.all()
    serializer_class = BusSerializer