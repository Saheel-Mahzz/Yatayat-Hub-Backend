from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet

router = DefaultRouter()
# Router ma viewset register gareko:
router.register(r'register', RegisterViewSet, basename='register')

urlpatterns = [
    # Yo line le 'api/register/' endpoint aafai banaudinchha
    path('', include(router.urls)), 
]