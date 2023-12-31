#vehiclepooling/views.py
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import VehicleListing, Booking
from .serializers import (
    VehicleListingSerializer, 
    RideListingLimitedSerializer, 
    RideDetailSerializer, 
    YourRideDetailsSerializer,
    EditRideSerializer,
    BookingSerializer,
    BookingListSerializer,
    BookingDetailSerializer,
)
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter
from datetime import datetime
from .permissions import IsOwnerOfBooking, IsOwnerOfRide
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from student.models import Student
from rest_framework import serializers, request
from django.utils import timezone
from django.db.models import Q
import pytz
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.template.loader import render_to_string


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

        # Exclude rides with zero available seats
        queryset = queryset.exclude(seats_available=0)
        
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
        


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BookRideView(CreateAPIView):
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Get the ride ID from the URL parameters
            ride_id = kwargs.get('pk', None)
            if not ride_id:
                raise serializers.ValidationError({"ride": "Ride ID is required."})

            # Get the ride instance
            ride = VehicleListing.objects.get(id=ride_id)

            # Check if the person trying to book is the owner of the ride
            if ride.owner == self.request.user.student_profile:
                raise PermissionDenied("You cannot book your own ride.")

            # Check if there are available seats
            num_seats_requested = int(request.data.get('num_seats', 1))
            if num_seats_requested > ride.seats_available:
                raise serializers.ValidationError({"detail": "Not enough available seats."})

            # Update ride information (reduce available seats)
            ride.seats_available -= num_seats_requested
            ride.save()

            # Create a booking record
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            booking = serializer.save(ride=ride, passenger=self.request.user.student_profile)

            # Build the success message
            success_message = f"{booking.passenger.user.get_full_name()} booked {num_seats_requested} seats of {ride.owner.user.get_full_name()}'s ride (id = {ride.id})"

            # Include the ride instance in the success response
            response_data = {
                "detail": success_message,
                "ride": {
                    "id": ride.id,
                    "owner_name": ride.owner.user.get_full_name(),
                    "from_location": ride.from_location,
                    "to_location": ride.to_location,
                    "start_date": ride.start_date,
                    "start_time": ride.start_time,
                    # Include other ride details as needed
                }
            }

            # Send email notification to the ride owner
            self.send_booking_notification_email(ride, ride.owner, booking.passenger, num_seats_requested)

            return Response(response_data, status=status.HTTP_201_CREATED)

        except VehicleListing.DoesNotExist:
            return Response({"detail": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as e:
        #     return Response({"detail": "An error occurred while processing the request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def send_booking_notification_email(self, ride, ride_owner, passenger, num_seats_booked):
        # Build the context for the email template
        context = {
            'owner_full_name': ride_owner.user.get_full_name(),
            'passenger_full_name': passenger.user.get_full_name(),
            'passenger_batch': f"{passenger.joining_year} - {passenger.passout_year} batch",
            'passenger_branch': passenger.branch,
            'num_seats': num_seats_booked,
            'passenger_contact_number': passenger.phone_number,
            'from_location': ride.from_location,
            'to_location': ride.to_location,
            'start_date': ride.start_date,
            'start_time': ride.start_time,
        }

        # Render the email body from the template
        email_body = render_to_string('booking_notification.txt', context)

        # Send the email
        send_mail(
            'Ride Booking Notification',
            email_body,
            'cambuzz03@gmail.com',  # Your sender email
            [ride_owner.user.email],  # Recipient's email
            fail_silently=False,
        )


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsOwnerOfBooking])
class MyBookingsListView(ListAPIView):
    serializer_class = BookingListSerializer

    def get_queryset(self):
        user_bookings = Booking.objects.filter(passenger=self.request.user.student_profile)
        return user_bookings

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"detail": "You haven't booked any rides yet."}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsOwnerOfBooking])
class MyBookingDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookingDetailSerializer
    queryset = Booking.objects.all()



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsOwnerOfBooking])
class EditBookingView(UpdateAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def get_object(self):
        booking_id = self.kwargs.get('pk')
        return Booking.objects.get(id=booking_id, passenger=self.request.user.student_profile)

    def update(self, request, *args, **kwargs):
        try:
            # Get the existing booking
            booking = self.get_object()
            # Get the updated number of seats
            old_num_seat = booking.num_seats
            num_seats_updated = int(request.data.get('num_seats', booking.num_seats))
            total_seats = booking.ride.seats_available + old_num_seat
            # Check if the updated number of seats is valid
            if (num_seats_updated) > total_seats:
                raise serializers.ValidationError({"detail": "Not enough available seats."})

            # Calculate the difference in seats
            seats_difference = num_seats_updated - booking.num_seats

            # Update the overall available seats of the ride
            booking.ride.seats_available -= seats_difference
            booking.ride.save()

            # Update the booking
            serializer = self.get_serializer(booking, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Build the success message
            success_message = f"{booking.passenger.user.get_full_name()} edited thier number of seats from {old_num_seat} to {num_seats_updated} of {booking.ride.owner.user.get_full_name()}'s ride (id = {booking.ride.id})"

            # Send email to the ride owner about the seat update
            self.send_seat_update_email(booking, old_num_seat, num_seats_updated)

            return Response({'detail':success_message}, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


    def send_seat_update_email(self, booking, old_num_seats, num_seats_updated):
        ride = booking.ride
        ride_owner_email = ride.owner.user.email

        # Construct email subject and message
        subject = 'Seat Update for Your Ride'
        message = render_to_string('booking_update_email.txt', {
            'passenger_name': booking.passenger.user.get_full_name(),
            'ride_details': f"{ride.from_location} to {ride.to_location} on {ride.start_date} at {ride.start_time}",
            'old_num_seats': old_num_seats,
            'new_num_seats': num_seats_updated,
            'ride_owner_name': booking.ride.owner.user.get_full_name()
        })

        # Send the email
        send_mail(subject, message, 'cambuzz03@gmail.com', [ride_owner_email])



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsOwnerOfBooking])
class CancelBookingView(DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            booking = self.get_object()

            # Store the number of seats for later use
            num_seats_cancelled = booking.num_seats

            # Update the overall available seats of the ride
            booking.ride.seats_available += num_seats_cancelled
            booking.ride.save()

            # Send email to the ride owner about the cancellation
            self.send_cancellation_email(booking, num_seats_cancelled)

            # Return success message
            success_message = f"You ({booking.passenger.user.get_full_name()}) have successfully cancelled your booking on {booking.ride.owner.user.get_full_name()}'s ride from {booking.ride.from_location} to {booking.ride.to_location} on {booking.ride.start_date} at {booking.ride.start_time}"

            # Continue with the booking cancellation
            super().destroy(request, *args, **kwargs)

            return Response({'detail': success_message}, status=status.HTTP_200_OK)


        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)
     
    def send_cancellation_email(self, booking, num_seats_cancelled):
        ride = booking.ride
        ride_owner_email = ride.owner.user.email

        # Construct email subject and message
        subject = 'Booking Cancellation for Your Ride'
        message = render_to_string('booking_cancellation.txt', {
            'passenger_name': booking.passenger.user.get_full_name(),
            'ride_details': f"{ride.from_location} to {ride.to_location} on {ride.start_date} at {ride.start_time}",
            'num_seats_cancelled': num_seats_cancelled,
            'ride_owner_name': booking.ride.owner.user.get_full_name()
        })

        # Send the email
        send_mail(subject, message, 'cambuzz03@gmail.com', [ride_owner_email])


