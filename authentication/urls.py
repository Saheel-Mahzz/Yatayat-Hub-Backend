from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AllUserProfile, RegisterViewSet, UserManagementViewSet, UserProfileView

router = DefaultRouter()
# Router ma viewset register gareko:
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'user', UserManagementViewSet, basename='user-management')
router.register(r'users', AllUserProfile, basename='all-users')

urlpatterns = [
    # Yo line le 'api/register/' endpoint aafai banaudinchha
    path('profile/me/', UserProfileView.as_view(), name='user-profile'),
    # path('users/', AllUserProfile.as_view(), name='all-users'),
    path('', include(router.urls)), 
]