from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # Password response ma na-dekhrauna ko lagi

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    # Data database ma halnu bhanda paila yo run hunchha:
    def create(self, validated_data):
        # Hami le paila banayeko custom manager ko 'create_user' call gareko:
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user