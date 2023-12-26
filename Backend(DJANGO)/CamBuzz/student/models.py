#student/models.py
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from accounts.models import CustomUser

class Student(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True, related_name='student_profile',)
    joining_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(date.today().year)],
        null=True,
        blank=True
    )
    passout_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(date.today().year + 4)]
    )
    branch_choices = (
        ('CSBS', 'CSBS'),
        ('AI&DS', 'AI&DS'),
        ('IT', 'IT'),
        ('ME', 'ME'),
        ('CE', 'CE'),
        ('CSE', 'CSE'),
        ('EEE', 'EEE'),
        ('ECE', 'ECE'),
        ('AEI', 'AEI'),
    )
    branch = models.CharField(max_length=10, choices=branch_choices)
    division_choices = (
        ('N/A', 'N/A'),
        ('Alpha', 'Alpha'),
        ('Beta', 'Beta'),
        ('Gamma', 'Gamma'),
    )
    division = models.CharField(max_length=10, choices=division_choices)
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    gender = models.CharField(max_length=10, choices=gender_choices)
    phone_number=models.CharField(max_length=15, null=True, blank=True)
    photo = models.ImageField(upload_to='media/profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    

# # Add related_name to avoid clashes
# Student._meta.get_field('groups').remote_field.related_name = 'student_groups'
# Student._meta.get_field('user_permissions').remote_field.related_name = 'student_user_permissions'

