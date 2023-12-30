from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer, ViewEventsSerializer, ViewEventDetailsSerializer
from .permissions import IsOrganisation
from datetime import datetime
from django.db.models import Q

class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOrganisation]

    def perform_create(self, serializer):
        # Set the organisation field before saving
        serializer.save(organisation=self.request.user.organisation_profile)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        event_name = response.data.get("event_name", "")
        organisation_name = request.user.organisation_profile.user.first_name
        success_message = f"You({organisation_name}) have added the event {event_name}!"
        response.data["detail"] = success_message
        return response


class EventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOrganisation]

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs['pk'])

        # Check if the requesting organisation is the one that added the event
        if self.request.user.organisation_profile == obj.organisation:
            return obj
        else:
            self.permission_denied(
                self.request, message=f"You ({self.request.user.organisation_profile.user.first_name}) do not have permission to update this event ({obj.event_name})."
            )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Success message
        success_message = f"Event updation (by {instance.organisation.user.first_name}) successful!"
        return Response({"detail": success_message})
    

class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOrganisation]

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs['pk'])

        # Check if the requesting organisation is the one that added the event
        if self.request.user.organisation_profile == obj.organisation:
            return obj
        else:
            self.permission_denied(
                self.request, message="You do not have permission to delete this event."
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the requesting organisation is the one that added the event
        if request.user.organisation_profile == instance.organisation:
            instance.delete()
            event_name = instance.event_name

            response_data = {
                "detail": f"{instance.organisation.user.first_name} deleted the event {event_name} successfully!"
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"detail": "You do not have permission to delete this event."},
                status=status.HTTP_403_FORBIDDEN
            )
        

class YourEventsView(generics.ListAPIView):
    serializer_class = ViewEventsSerializer
    permission_classes = [IsAuthenticated, IsOrganisation]

    def get_queryset(self):
        organisation = self.request.user.organisation_profile
        current_time = datetime.now()

        # Retrieve upcoming and past events for the organisation
        upcoming_events = Event.objects.filter(
            Q(organisation=organisation, start_date__gt=current_time.date()) |  # Events with future dates
            Q(organisation=organisation, start_date=current_time.date(), start_time__gte=current_time.time())  # Events starting today after current time
        ).order_by('start_date', 'start_time')

        past_events = Event.objects.filter(
            Q(organisation=organisation, start_date__lt=current_time.date()) |  # Events with past dates
            Q(organisation=organisation, start_date=current_time.date(), start_time__lt=current_time.time())  # Events starting today before current time
        ).order_by('-start_date', '-start_time')

        return {
            'upcoming_events': upcoming_events,
            'past_events': past_events
        }

    def list(self, request, *args, **kwargs):
        queryset_dict = self.get_queryset()

        organisation_name = request.user.organisation_profile.user.first_name

        response_data = {
            'organisation_name': organisation_name,
            'upcoming_events': self.get_serializer(queryset_dict['upcoming_events'], many=True).data,
            'past_events': self.get_serializer(queryset_dict['past_events'], many=True).data,
        }

        return Response(response_data, status=status.HTTP_200_OK)



class ViewEventsView(generics.ListAPIView):
    serializer_class = ViewEventsSerializer

    def get_queryset(self):
        current_time = datetime.now()
        organisation_name = self.request.query_params.get('organisation_name', None)
        date_filter = self.request.query_params.get('date', None)

        # Retrieve upcoming and past events
        upcoming_events = Event.objects.filter(
            Q(start_date__gt=current_time.date()) |  # Events with future dates
            Q(start_date=current_time.date(), start_time__gte=current_time.time())  # Events starting today after current time
        ).order_by('start_date', 'start_time')

        past_events = Event.objects.filter(
            Q(start_date__lt=current_time.date()) |  # Events with past dates
            Q(start_date=current_time.date(), start_time__lt=current_time.time())  # Events starting today before current time
        ).order_by('-start_date', '-start_time')

        # Apply additional filters if provided
        if organisation_name:
            upcoming_events = upcoming_events.filter(organisation__user__first_name__iexact=organisation_name)
            past_events = past_events.filter(organisation__user__first_name__iexact=organisation_name)

        if date_filter:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            upcoming_events = upcoming_events.filter(start_date=date_obj)
            past_events = past_events.filter(start_date=date_obj)

        return {
            'upcoming_events': upcoming_events,
            'past_events': past_events
        }

    def list(self, request, *args, **kwargs):
        queryset_dict = self.get_queryset()

        upcoming_events_data = self.get_serializer(queryset_dict['upcoming_events'], many=True).data
        past_events_data = self.get_serializer(queryset_dict['past_events'], many=True).data

        # Include organization name for each event
        for event_data in upcoming_events_data:
            event_data['organisation_name'] = event_data['organisation_name']

        for event_data in past_events_data:
            event_data['organisation_name'] = event_data['organisation_name']

        response_data = {
            'upcoming_events': upcoming_events_data,
            'past_events': past_events_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

class ViewEventDetailsView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = ViewEventDetailsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'event_details': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
