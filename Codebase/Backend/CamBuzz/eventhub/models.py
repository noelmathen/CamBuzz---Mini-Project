# eventhub/models.py
from django.db import models
from organisations.models import Organisation

class Event(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    registration_link = models.URLField(blank=True, null=True)
    poster = models.ImageField(upload_to='event_posters/', blank=False, null=True)
    people_interested = models.IntegerField(default=0)

    def __str__(self):
        return self.event_name
    
    def update_event(self, **kwargs):
        # Update event details
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()

    def delete_event(self):
        # Delete the event
        self.delete()
