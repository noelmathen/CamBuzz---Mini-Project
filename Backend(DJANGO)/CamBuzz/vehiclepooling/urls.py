#vehiclepooling/urls.py
from django.urls import path
from .views import (
    PublishRideView, 
    FindRideView, 
    RideDetailView, 
    YourRidesView, 
    EditRideView, 
    DeleteRideView,
    BookRideView,
    MyBookingsListView,
    MyBookingDetailView,
    EditBookingView,
    CancelBookingView,
)

urlpatterns = [
    path('publish-ride/', PublishRideView.as_view(), name='publish-ride'),
    path('find-ride/', FindRideView.as_view(), name='find-ride'),
    path('rides/<int:pk>/', RideDetailView.as_view(), name='ride-detail'),
    path('rides/<int:pk>/book/', BookRideView.as_view(), name='book-ride'),
    path('your-rides/', YourRidesView.as_view(), name='your-rides'),
    path('your-rides/<int:pk>/edit/', EditRideView.as_view(), name='edit-ride'),
    path('your-rides/<int:pk>/delete/', DeleteRideView.as_view(), name='delete-ride'),
    path('my_bookings/', MyBookingsListView.as_view(), name='my-bookings-list'),
    path('my_bookings/<int:pk>/', MyBookingDetailView.as_view(), name='my-booking-detail'),
    path('my_bookings/<int:pk>/edit/', EditBookingView.as_view(), name='edit-booking'),
    path('my_bookings/<int:pk>/cancel/', CancelBookingView.as_view(), name='cancel-booking'),
]

