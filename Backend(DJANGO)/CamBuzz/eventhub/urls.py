# organisations/urls.py
from django.urls import path, include
from .views import (
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    YourEventsView,
    ViewEventsView,
    ViewEventDetailsView,
)

urlpatterns = [
    path('addevent/', EventCreateView.as_view(), name='add_event'),
    path('updateevent/<int:pk>/', EventUpdateView.as_view(), name='update_event'),
    path('deleteevent/<int:pk>/', EventDeleteView.as_view(), name='delete_event'),
    path('yourevents/', YourEventsView.as_view(), name='your_events'),
    path('viewevents/', ViewEventsView.as_view(), name='view_events'),
    path('vieweventdetails/<int:pk>/', ViewEventDetailsView.as_view(), name='view_event_details'),
]
