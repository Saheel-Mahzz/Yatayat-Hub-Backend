from rest_framework import serializers

from bookings.models import BookedSeats, Booking, BookingBusModel, Location, Trip
from django.contrib.auth import get_user_model

User = get_user_model()
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']  
class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingBusModel
        fields = '__all__' # Yesle bus ko sabai parameters JSON banaundinchha
        
class TripReadSerializer(serializers.ModelSerializer):
    bus = BusSerializer(read_only=True)  
    from_location = serializers.StringRelatedField(read_only=True)
    to_location = serializers.StringRelatedField(read_only=True)
    booked_seats = serializers.SerializerMethodField()
    class Meta:
        model = Trip
        fields = "__all__"       
    
    def get_booked_seats(self,obj):
        # return Booking.objects.filter(trip=obj).values_list('seat_number',flat=True)   
        return  BookedSeats.objects.filter(booking__trip=obj).values_list('seat_number', flat=True)   

class BookingSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    trip = TripReadSerializer(read_only=True)
    seats = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='seat_number',
        source='bookedseats_set'  # Yedi model ma related_name="booked_seats" cha bhane tyo rakhne
    )
    
    class Meta:
        model = Booking
        fields = '__all__' # Yesle booking ko parameters handle garchha
        
class BookingWriteSerializer(serializers.ModelSerializer):
    seat_number = serializers.ListField(
        child=serializers.CharField(max_length=10),
        write_only=True
    )
    class Meta:
        model = Booking
        # fields = '__all__' 
        fields = ['id', 'user', 'trip', 'seat_number', 'booked_at'] 
        read_only_fields = ['user','booked_at']# Yesle booking ko parameters handle garchha
        
    def validate(self, attrs):
        trip = attrs.get('trip')
        seat_number = attrs.get('seat_number')
        
        user = self.context['request'].user
        
        existing_seats_count = BookedSeats.objects.filter(
            booking__trip=trip,
            booking__user=user
        ).count()
        
        total_requested_seats = existing_seats_count + len(seat_number)
        
        if total_requested_seats > 5:
            remaining_seats = 5 - existing_seats_count
            if remaining_seats <= 0:
                raise serializers.ValidationError("Rukau! Tapai le already 5 seats book garnu bhaisaknu bhayo.")
            else:
                raise serializers.ValidationError(f"Rukau! Tapai le matra {remaining_seats} seat haru book garna saknu hunchha.")
            
        # Check 1: User le empty list ta pathaeko chhaina?
        if not seat_number:
            raise serializers.ValidationError("Atleast One seat must be selected for booking.")

        # Check 2: Max limit (e.g. Max 5 seats)
        if len(seat_number) > 5:
            raise serializers.ValidationError("Atleast One seat must be selected for booking.")

        # Check 3: Database ma yo trip ko seat paile nai book chha ki nai?
        already_booked = BookedSeats.objects.filter(
            booking__trip=trip,
            seat_number__in=seat_number
        ).exists()

        if already_booked:
            raise serializers.ValidationError("Rukau! Yaha madhye kunai seat haru paile nai book bhaisakeko chha.")

        return attrs    
    def create(self, validated_data):
        # List field lai pop garera chuttaune
        seat_number = validated_data.pop('seat_number')

        # Main Booking Entry create garne
        booking = Booking.objects.create(**validated_data)

        # Loop lagayera dynamic Seats Entry garne
        
        booked_seat_objects=[
            BookedSeats(booking=booking, seat_number=seat) for seat in seat_number
        ]
        BookedSeats.objects.bulk_create(booked_seat_objects)

        return booking
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'          
        
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'        
        
class BusDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingBusModel
        fields = ['id','name']    
        
 
        
class TripWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"        