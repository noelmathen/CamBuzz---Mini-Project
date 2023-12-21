from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are only allowed to the owner of the ride.
        allowed = obj.owner == request.user
        print(f"Request User: {request.user}")
        print(f"Object Owner: {obj.owner}")
        print(f"Allowed: {allowed}")
        return allowed
    
    
class IsOwnerOfRide(BasePermission):
    message = "You do not have permission to edit this ride."

    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the owner of the ride
        return obj.owner == request.user.student_profile
    

class IsOwnerOfBooking(BasePermission):
    message = "You do not have permission to view/modify/delete this booking."

    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the passenger associated with the booking
        return obj.passenger == request.user.student_profile
    

