#vehiclepooling/urls.py
from django.urls import path
from .views import PublishRideView, FindRideView, RideDetailView, YourRidesView, EditRideView, DeleteRideView

urlpatterns = [
    path('publish-ride/', PublishRideView.as_view(), name='publish-ride'),
    path('find-ride/', FindRideView.as_view(), name='find-ride'),
    path('rides/<int:pk>/', RideDetailView.as_view(), name='ride-detail'),
    path('your-rides/', YourRidesView.as_view(), name='your-rides'),
    path('your-rides/<int:pk>/edit/', EditRideView.as_view(), name='edit-ride'),
    path('your-rides/<int:pk>/delete/', DeleteRideView.as_view(), name='delete-ride'),
]


