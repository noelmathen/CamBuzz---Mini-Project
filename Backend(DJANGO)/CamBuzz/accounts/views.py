from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileUpdateSerializer, ChangePasswordSerializer, DeleteAccountSerializer
from .permissions import IsOwnerOrReadOnly


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # Automatically calculate passout year
            joining_year = serializer.validated_data['joining_year']
            serializer.validated_data['passout_year'] = joining_year + 4

            # Create the user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            response_data = {
                "message": f"Login Successful! Welcome {user.first_name} {user.last_name}!",
                "user_name": f"{user.first_name} {user.last_name}",  # Include the user's name
                "user_token": token.key,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        first_name = request.user.first_name
        request.auth.delete()
        return Response({"detail": f"Goodbye {first_name}, Logout successful!"}, status=status.HTTP_200_OK)


class UserProfileUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        first_name = request.user.first_name
        # Check if the user making the request is the owner of the profile being updated
        if serializer.is_valid() and user == serializer.instance:
            serializer.save()
            return Response({"detail": f"{first_name}'s profile updated successfully."}, status=status.HTTP_200_OK)
        
        return Response({"detail": f"{first_name} is unauthorized to update this profile."}, status=status.HTTP_403_FORBIDDEN)
    

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        first_name = user.first_name
        if serializer.is_valid():
            try:
                user.change_password(serializer.validated_data['current_password'], serializer.validated_data['new_password'])
                return Response({"detail": f"{first_name}'s password is changed successfully."}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def post(self, request):
        user = request.user
        serializer = DeleteAccountSerializer(data=request.data)
        first_name = user.first_name

        if serializer.is_valid():
            try:
                # Ensure that the user requesting the deletion is the owner of the account
                self.check_object_permissions(request, user)
                user.delete_account(serializer.validated_data['password'])
                return Response({"detail": f"{first_name}'s account deleted successfully."}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


