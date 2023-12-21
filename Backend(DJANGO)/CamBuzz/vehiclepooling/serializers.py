#vehiclepooling/serializers.py
from rest_framework import serializers
from .models import VehicleListing, Booking

class VehicleListingSerializer(serializers.ModelSerializer):
    # owner = StudentProfileSerializer()
    class Meta:
        model = VehicleListing
        fields = '__all__'
        read_only_fields = ('owner',)


class RideListingLimitedSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    from_location_start_datetime = serializers.SerializerMethodField()
    to_location_end_datetime = serializers.SerializerMethodField()

    class Meta:
        model = VehicleListing
        fields = ['id', 'owner', 'from_location_start_datetime', 'to_location_end_datetime', 'vehicle_type', 'seats_available', 'price']

    def get_owner(self, obj):
        owner = obj.owner  
        return f"{owner.user.first_name} ({owner.branch})"


    def get_from_location_start_datetime(self, obj):
        return f"{obj.from_location} ({obj.start_date} {obj.start_time})"

    def get_to_location_end_datetime(self, obj):
        return f"{obj.to_location} ({obj.end_date} {obj.end_time})"
    

class RideDetailSerializer(serializers.ModelSerializer):
    owner_details = serializers.SerializerMethodField()
    vehicle_details = serializers.SerializerMethodField()

    class Meta:
        model = VehicleListing
        fields = [
            'from_location', 'to_location', 'start_date', 'end_date', 'start_time', 'end_time',
            'owner_details', 'vehicle_details', 'price', 'description'
        ]

    def get_owner_details(self, obj):
        owner = obj.owner
        return {
            'full_name': owner.user.get_full_name(),
            'phone_number': owner.phone_number,
            'branch': owner.branch,
            'division': owner.division,
            'batch': f"{owner.joining_year} - {owner.passout_year} batch",
            'gender': owner.get_gender_display()
        }

    def get_vehicle_details(self, obj):
        return {
            'vehicle_type': obj.vehicle_type,
            'vehicle_name': obj.vehicle_name,
            'vehicle_number': obj.vehicle_number,
            'seats': obj.seats_available,
            'extra_helmet': obj.extra_helmet
        }
    

class YourRideDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleListing
        fields = '__all__'
        read_only_fields = ( 'from_location', 'to_location', 'start_date', 'end_date', 'start_time', 'end_time', 'description')
    def get_owner_details(self, obj):
        owner = obj.owner
        return {
            'owner': f"{owner.get_full_name()} ({owner.pk})",
            'vehicle_type': obj.vehicle_type,
            'vehicle_name': obj.vehicle_name,
            'vehicle_number': obj.vehicle_number,
            'seats': obj.seats_available,
            'extra_helmet': obj.extra_helmet,
            'from_location': obj.from_location,
            'to_location': obj.to_location,
            'start_date': obj.start_date,
            'end_date': obj.end_date,
            'start_time': obj.start_time,
            'end_time': obj.end_time,
            'price': obj.price,
            'description': obj.description,
        }
    

class EditRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleListing
        fields = '__all__'
        read_only_fields = ('owner',)


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('num_seats',)


class BookingListSerializer(serializers.ModelSerializer):
    ride_details = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'num_seats', 'created_at', 'ride_details']

    def get_ride_details(self, obj):
        ride = obj.ride
        return {
            'owner_name': ride.owner.user.get_full_name(),
            'start_location': ride.from_location,
            'start_date': ride.start_date,
            'start_time': ride.start_time,
            'end_location': ride.to_location,
            'end_date': ride.end_date,
            'end_time': ride.end_time,
            'price': ride.price,
        }


class BookingDetailSerializer(serializers.ModelSerializer):
    ride_details = serializers.SerializerMethodField()
    ride_owner_details = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['num_seats', 'created_at', 'ride_owner_details', 'ride_details']

    def get_ride_details(self, obj):
        ride = obj.ride
        return {
            'from_location': ride.from_location,
            'to_location': ride.to_location,
            'start_date': ride.start_date,
            'start_time': ride.start_time,
            'end_date': ride.end_date,
            'end_time': ride.end_time,
            'vehicle_type': ride.vehicle_type,
            'vehicle_name': ride.vehicle_name,
            'vehicle_number': ride.vehicle_number,
            'price': ride.price,
            'description': ride.description,
            # 'seats_available': ride.seats_available,
        }

    def get_ride_owner_details(self, obj):
        owner = obj.ride.owner
        return {
            'ride_owner_name': owner.user.get_full_name(),
            'ride_owner_batch': f"{owner.joining_year} - {owner.passout_year} batch",
            'ride_owner_branch': owner.branch,
            'ride_owner_phone_number': owner.phone_number,
        }



