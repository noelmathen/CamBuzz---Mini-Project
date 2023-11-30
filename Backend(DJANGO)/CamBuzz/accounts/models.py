from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password, check_password

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    # Mandatory Fields
    first_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)  # Adjust the max length as needed
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)

    password = models.CharField(max_length=128)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    # Additional Fields
    last_name = models.CharField(max_length=30, blank=True, null=True)
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
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def change_password(self, current_password, new_password):
        # Check if the current password is correct
        if not check_password(current_password, self.password):
            raise ValueError("Current password is incorrect.")

        # Update the password with the new one
        self.set_password(new_password)
        self.save()


    def delete_account(self, password):
        # Check if the provided password is correct
        if not check_password(password, self.password):
            raise ValueError("Incorrect password. Account deletion failed.")

        # Perform any additional cleanup or actions before deleting the account (if needed)
        # For example, you might want to delete related data or perform other cleanup actions.

        # Delete the user account
        self.delete()


# Add related_name to avoid clashes
CustomUser._meta.get_field('groups').remote_field.related_name = 'customuser_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'customuser_user_permissions'