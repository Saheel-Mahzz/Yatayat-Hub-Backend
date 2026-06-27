from rest_framework.routers import DefaultRouter
from django.urls import path, include

from bookings.views import BusViewSets

router = DefaultRouter()

router.register(r'buses',BusViewSets,basename='bus')

urlpatterns = [
    # Router ko sabai endpoints lai local layout ma haleko
    path('', include(router.urls)),
]