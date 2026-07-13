from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, UserManagementViewSet, UserProfileView

router = DefaultRouter()
# Router ma viewset register gareko:
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'user', UserManagementViewSet, basename='user-management')

urlpatterns = [
    # Yo line le 'api/register/' endpoint aafai banaudinchha
    path('profile/me/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)), 
]