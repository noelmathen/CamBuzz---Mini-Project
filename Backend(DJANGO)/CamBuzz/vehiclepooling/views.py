#vehiclepooling/views.py
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import VehicleListing
from .serializers import (
    VehicleListingSerializer, 
    RideListingLimitedSerializer, 
    RideDetailSerializer, 
    YourRideDetailsSerializer,
    EditRideSerializer,
)
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter
from datetime import datetime
from .permissions import IsOwnerOrReadOnly, IsOwnerOfRide
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from student.models import Student
from rest_framework import serializers, request
from django.utils import timezone
from django.db.models import Q
import pytz

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PublishRideView(CreateAPIView):
    queryset = VehicleListing.objects.all()
    serializer_class = VehicleListingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Get the start and end date and time from the serializer
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']

        # Check if end date is before start date or end time is before start time
        if end_date < start_date:
            raise serializers.ValidationError({"detail": "End date must be on or after the start date."})
        elif end_time <= start_time:
            raise serializers.ValidationError({"detail": "End time must be after the start time"})
        
        # Create a Student instance from the CustomUser instance
        student_instance = Student.objects.get(user=self.request.user)
        serializer.save(owner=student_instance)


class FindRideView(ListAPIView):
    queryset = VehicleListing.objects.all()
    serializer_class = RideListingLimitedSerializer
    filter_backends = [OrderingFilter]

    def get_queryset(self):
        from_location = self.request.query_params.get('from_location', '')
        to_location = self.request.query_params.get('to_location', '')
        date_param = self.request.query_params.get('date', '')

        # Parse the date parameter to a datetime object
        try:
            date = datetime.strptime(date_param, '%Y-%m-%d')
        except ValueError:
            date = datetime.now()

        # Set the timezone to Asia/Kolkata
        local_tz = pytz.timezone('Asia/Kolkata')
        date = local_tz.localize(date)

        # Build a queryset that filters based on from_location, to_location, and date
        queryset = VehicleListing.objects.filter(start_date__gte=date)

        if from_location:
            queryset = queryset.filter(from_location__icontains=from_location)

        if to_location:
            queryset = queryset.filter(to_location__icontains=to_location)

        # Exclude rides that have already started
        today = local_tz.localize(datetime.now()).date()
        current_time = local_tz.localize(datetime.now()).time()
        queryset = queryset.exclude(
            Q(start_date__lt=today) |
            (Q(start_date=today) & Q(start_time__lte=current_time))
        )

        return queryset.order_by('start_date', 'start_time')


class RideDetailView(RetrieveAPIView):
    queryset = VehicleListing.objects.all()
    serializer_class = RideDetailSerializer


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class YourRidesView(ListAPIView):
    serializer_class = YourRideDetailsSerializer
    filter_backends = [OrderingFilter]
    ordering = ['owner']

    def get_queryset(self):
        student_instance = Student.objects.get(user=self.request.user)
        today = datetime.now().date()
        return VehicleListing.objects.filter(owner=student_instance, start_date__gte=today)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsOwnerOfRide])
class EditRideView(RetrieveUpdateAPIView):
    queryset = VehicleListing.objects.all()
    serializer_class = EditRideSerializer



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsOwnerOfRide])
class DeleteRideView(DestroyAPIView):
    queryset = VehicleListing.objects.all()
    serializer_class = YourRideDetailsSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        owner_name = instance.owner.user.get_full_name()  # Assuming you have a method to get the full name of the owner

        try:
            ride_id = instance.id
            self.perform_destroy(instance)
            return Response(
                {"detail": f"Ride number {ride_id} published by {owner_name} is successfully deleted."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"detail": f"Deletion of the ride {ride_id} failed, please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

