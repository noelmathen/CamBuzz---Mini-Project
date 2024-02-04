#foodrecommendation/admin.py
from django.contrib import admin
from .models import Restaurant, Recommendation

admin.site.register(Restaurant)
admin.site.register(Recommendation)