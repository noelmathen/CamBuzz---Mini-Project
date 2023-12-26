from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import login, authenticate
from .serializers import (
    LoginSerializer,
    ChangePasswordSerializer,
    DeleteAccountSerializer,
)
from django.middleware.csrf import get_token


class LoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        csrf_token = get_token(request)

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        is_student = serializer.validated_data['is_student']
        is_organisation = serializer.validated_data['is_organisation']
        # Check user type in CustomUser model
        user = None
        if is_student and CustomUser.objects.filter(username=username, is_student=True).exists():
            user = authenticate(request, username=username, password=password)
        elif is_organisation and CustomUser.objects.filter(username=username, is_organisation=True).exists():
            user = authenticate(request, username=username, password=password, is_organisation=True)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                'message': f'Login Successful: Welcome {user.first_name}' if user.first_name else f'Login Successful',
                'user_type': 'Student' if is_student else 'Organisation',
                'token': token.key,
                'first_name': user.first_name,
                'photo_url': user.student_profile.photo.url if is_student else user.organisation_profile.photo.url,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials or user type'}, status=status.HTTP_401_UNAUTHORIZED)
        

class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        first_name = request.user.first_name
        request.auth.delete()
        return Response({"detail": f"Goodbye {first_name}, Logout successful!"}, status=status.HTTP_200_OK)
    

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

