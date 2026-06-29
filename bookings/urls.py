from rest_framework.routers import DefaultRouter
from django.urls import path, include

from bookings.views import BookingViewSets, BusViewSets, TripViewSets

router = DefaultRouter()

router.register(r'buses',BusViewSets,basename='bus')
router.register(r'bookings', BookingViewSets, basename='booking')
router.register(r'trips', TripViewSets, basename='trip')

urlpatterns = [
    # Router ko sabai endpoints lai local layout ma haleko
    path('', include(router.urls)),
]