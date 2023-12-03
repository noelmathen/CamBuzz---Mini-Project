# authentication/models.py
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from accounts.models import CustomUser

class AdminUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        pass

    def create_superuser(self, email, password=None, **extra_fields):
        # Call the base method to create a superuser
        user = self.create_user(email, password, **extra_fields)

        # Set additional fields for a superuser
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True  # Set your custom 'is_admin' field to True

        # Save the user
        user.save(using=self._db)
        return user






























# # authentication/models.py
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models
# from django.utils import timezone
# from accounts.models import CustomUser

# class AdminUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self.create_user(email, password, **extra_fields)

# class AdminUser(AbstractBaseUser, PermissionsMixin):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, )

#     # Add any other fields you need for the admin user

#     objects = AdminUserManager()

#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email

#     class Meta:
#         # Add related_name to avoid clashes
#         permissions = [
#             ('view_custom_adminuser', 'Can view Custom AdminUser'),
#         ]

# # Add related_name to avoid clashes
# AdminUser._meta.get_field('groups').remote_field.related_name = 'adminuser_groups'
# AdminUser._meta.get_field('user_permissions').remote_field.related_name = 'adminuser_user_permissions'

