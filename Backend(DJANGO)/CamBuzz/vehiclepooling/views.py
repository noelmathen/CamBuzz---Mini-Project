from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import VehicleListing
from .serializers import VehicleListingSerializer, RideListingLimitedSerializer, RideDetailSerializer, YourRideDetailsSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter
from datetime import datetime
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework import status


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PublishRideView(CreateAPIView):
    queryset = VehicleListing.objects.all()
    serializer_class = VehicleListingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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

        # Build a queryset that filters based on from_location, to_location, and date
        queryset = VehicleListing.objects.filter(start_time__date__gte=date)

        if from_location:
            queryset = queryset.filter(from_location__icontains=from_location)

        if to_location:
            queryset = queryset.filter(to_location__icontains=to_location)

        return queryset


class RideDetailView(RetrieveAPIView):
    queryset = VehicleListing.objects.all()
    serializer_class = RideDetailSerializer


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class YourRidesView(ListAPIView):
    serializer_class = YourRideDetailsSerializer
    filter_backends = [OrderingFilter]

    def get_queryset(self):
        user = self.request.user
        today = datetime.now().date()
        return VehicleListing.objects.filter(owner=user, start_time__date__gte=today)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
class EditRideView(RetrieveUpdateAPIView):
    queryset = VehicleListing.objects.all()
    serializer_class = YourRideDetailsSerializer



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
class DeleteRideView(DestroyAPIView):
    queryset = VehicleListing.objects.all()
    serializer_class = YourRideDetailsSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        owner_name = instance.owner.get_full_name()  # Assuming you have a method to get the full name of the owner

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
        


