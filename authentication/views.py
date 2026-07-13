from django.shortcuts import render
from rest_framework import generics, viewsets,mixins,status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.models import CustomUser, ProfileModel
from authentication.serializers import CustomTokenObtainPairSerializer, ProfileSerializer, RegisterSerializer

# Create your views here.
# class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = RegisterSerializer
    
#     def create(self,request,*args,**kwargs):
#         serializer

class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        # 1. Request bata aayeko data lai serializer ma pathaune
        serializer = self.get_serializer(data=request.data)
        
        # 2. Data valid chha ki chaina check garne (invalid bhaye automatic 400 error dinchha)
        serializer.is_valid(raise_exception=True)
        
        # 3. Serializer ko create method call garera user database ma save garne
        user = serializer.save()
        
        # 4. Save bhayeko user ko lagi JWT Token generate garne
        refresh = RefreshToken.for_user(user)
        
        # 5. User data ra Tokens lai mix garera response data ready parne
        custom_response_data = {
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        # 6. Frontend lai complete data return gardine
        return Response(custom_response_data, status=status.HTTP_201_CREATED)    
    
    
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]
               
    def get_object(self):
     return self.request.user.profile  
    
    # def get_queryset(self):
    #     return self.request.user.profile
    # def get_object(self):
    #     # Crash huna bata jogaune safe logic:
    #     # User ko profile chha bhane linchha, chaina bhane dynamically table ma create garcha!
    #     profile, created = ProfileModel.objects.get_or_create(user=self.request.user)
    #     return profile
     
        
        
class CustomTokenObtainPairView(TokenObtainPairView):
    # Default serializer badalera hamro custom serializer assign gareko:
    serializer_class = CustomTokenObtainPairSerializer        
    
class UserManagementViewSet(viewsets.ViewSet):
    # Logged-in user le matra chalauna paune
    permission_classes = [IsAuthenticated]

    # @action decorator thapera custom route banaune
    # detail=False bhanda url ma primary key id (like /api/user/1/change-password/) chahidaina, direct /api/user/change-password/ hunchha
    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        # 1. Verification Checking
        if not user.check_password(current_password):
            return Response({"error": "Current password milena!"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Update logic
        user.set_password(new_password)
        user.save()
        
        return Response({"message": "Password successfully change bhayo!"}, status=status.HTTP_200_OK)    