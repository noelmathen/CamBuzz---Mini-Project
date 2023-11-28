from rest_framework import serializers
from .models import VehicleListing

class VehicleListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleListing
        fields = '__all__'
        read_only_fields = ('owner',)


class RideListingLimitedSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    from_location_start_time = serializers.SerializerMethodField()
    to_location_eta = serializers.SerializerMethodField()

    class Meta:
        model = VehicleListing
        fields = ['id', 'owner', 'from_location_start_time', 'to_location_eta', 'vehicle_type', 'price']

    def get_owner(self, obj):
        return f"{obj.owner.first_name} ({obj.owner.branch})"

    def get_from_location_start_time(self, obj):
        return f"{obj.from_location} ({obj.start_time})"

    def get_to_location_eta(self, obj):
        return f"{obj.to_location} ({obj.eta})"
    

class RideDetailSerializer(serializers.ModelSerializer):
    owner_details = serializers.SerializerMethodField()
    vehicle_details = serializers.SerializerMethodField()

    class Meta:
        model = VehicleListing
        fields = [
            'from_location', 'to_location', 'start_time', 'eta', 'owner_details', 'vehicle_details', 
            'price', 'description'
        ]

    def get_owner_details(self, obj):
        owner = obj.owner
        return {
            'full_name': owner.get_full_name(),
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
        read_only_fields = ('owner',)



