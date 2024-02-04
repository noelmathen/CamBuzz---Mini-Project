#vehiclepooling/admin.py
from django.contrib import admin
from .models import VehicleListing, Booking

admin.site.register(VehicleListing)
admin.site.register(Booking)

