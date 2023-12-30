# eventhub/serializers.py
from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('event_name', 'start_date', 'end_date', 'start_time', 'end_time', 'location', 'description', 'registration_link', 'poster')

    def get_organisation_name(self, obj):
        return obj.organisation.user.first_name if obj.organisation else None



class ViewEventsSerializer(serializers.ModelSerializer):
    organisation_name = serializers.SerializerMethodField()

    class Meta:
        model = Event
        # fields = ('organisation_name', 'event_name', 'start_date', 'end_date', 'start_time', 'end_time', 'location', 'description', 'registration_link', 'poster')
        fields = ('id', 'organisation_name', 'event_name', 'poster')


    def get_organisation_name(self, obj):
        return obj.organisation.user.first_name if obj.organisation else None


class ViewEventDetailsSerializer(serializers.ModelSerializer):
    organisation_name = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('organisation_name', 'event_name', 'start_date', 'end_date', 'start_time', 'end_time', 'location', 'description', 'registration_link', 'poster')

    def get_organisation_name(self, obj):
        return obj.organisation.user.first_name if obj.organisation else None

