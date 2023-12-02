# organisations/permissions.py
from rest_framework import permissions

class IsActive(permissions.BasePermission):
    """
    Custom permission to check if the user is active.
    """
    def has_permission(self, request, view):
        # Assuming your user model has a field named 'is_active'
        user = request.user
        return user.is_active if user else False
    

