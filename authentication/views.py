from django.shortcuts import render
from rest_framework import generics, viewsets,mixins
from rest_framework.permissions import IsAuthenticated

from authentication.models import CustomUser, ProfileModel
from authentication.serializers import ProfileSerializer, RegisterSerializer

# Create your views here.
class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]
    
    # def get_queryset(self):
    #     return self.request.user.profile
    # def get_object(self):
    #     # Crash huna bata jogaune safe logic:
    #     # User ko profile chha bhane linchha, chaina bhane dynamically table ma create garcha!
    #     profile, created = ProfileModel.objects.get_or_create(user=self.request.user)
    #     return profile
           
    def get_object(self):
     return self.request.user.profile       
        