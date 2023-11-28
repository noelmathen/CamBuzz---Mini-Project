from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    joining_year = models.PositiveSmallIntegerField(blank=True, null=True)
    passout_year = models.PositiveSmallIntegerField(blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True)

