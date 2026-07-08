from rest_framework import serializers
from .models import CustomUser, ProfileModel
from django.contrib.auth import get_user_model

User = get_user_model()

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True) # Password response ma na-dekhrauna ko lagi

#     class Meta:
#         model = CustomUser
#         # fields = ('email', 'password')
#         fields = ('username', 'email', 'password', 'first_name', 'last_name')

#     # Data database ma halnu bhanda paila yo run hunchha:
#     def create(self, validated_data):
#         # Hami le paila banayeko custom manager ko 'create_user' call gareko:
#         user = CustomUser.objects.create_user(
#             email=validated_data['email'],
#             password=validated_data['password'],
#             first_name=validated_data.get('first_name', ''),
#             # username=validated_data.get('username', ''),
#             last_name=validated_data.get('last_name', '')
#         )
#         return user

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        # Fields ma 'phone_number' ra 'confirm_password' dubai thapera clear banayeko
        fields = ('email', 'password', 'confirm_password', 'phone_number', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password ra Confirm Password milena!"})
        return attrs

    def create(self, validated_data):
        # 1. Validation bhae sake pachi confirm_password lai pop garera faldine
        validated_data.pop('confirm_password', None)
        
        # 2. validated_data ko baaki sabai chiz (email, password, phone_number, etc.) direct pass hunchha
        # password lai hamro manager le extra_fields bhanda agadi nai handle garchha
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            **validated_data # Yesle phone_number, first_name, last_name sabai automatic manager ma pathaudinchha
        )
        return user
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']    
class ProfileSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)  # Nested serializer for user details
    class Meta:
        model = ProfileModel
        fields ="__all__"    