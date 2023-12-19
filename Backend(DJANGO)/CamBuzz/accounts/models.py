#accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
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
        extra_fields.setdefault('is_admin', True)
        return self.create_user(username, email, password, **extra_fields)
    

    def create_organisation_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_organisation', True)
        extra_fields.setdefault('is_active', False)
        return self.create_user(username, email,  password, **extra_fields)

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_organisation = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()
    # password = models.CharField(max_length=128)
    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)

    # def check_password(self, raw_password):
    #     return check_password(raw_password, self.password)


    def change_password(self, current_password, new_password):
        # Check if the current password is correct
        if not check_password(current_password, self.password):
            raise ValueError("Current password is incorrect.")
        self.set_password(new_password)
        self.save()


    def delete_account(self, password):
        # Check if the provided password is correct
        if not check_password(password, self.password):
            raise ValueError("Incorrect password. Account deletion failed.")
        self.delete()


# # Add related_name to avoid clashes
# CustomUser._meta.get_field('groups').remote_field.related_name = 'customuser_groups'
# CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'customuser_user_permissions'

