# organisations/views.py
from rest_framework import generics
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import OrganisationRegistrationRequest, Organisation
from accounts.models import CustomUser
from .serializers import (
    OrganisationRegistrationRequestSerializer, 
    OrganisationRegistrationSerializer, 
    OrganisationProfileEditSerializer,
    OrganisationListSerializer,
    OrganisationSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class OrganisationRegistrationRequestApproveView(generics.UpdateAPIView):
    queryset = OrganisationRegistrationRequest.objects.all()
    serializer_class = OrganisationRegistrationRequestSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = OrganisationRegistrationRequest.APPROVED
        instance.save()
        instance.organisation.user.is_active = True  # Set is_active to True upon approval
        instance.organisation.user.save()
        instance.send_approval_email()
        return Response({'detail': 'Registration request approved successfully.'}, status=status.HTTP_200_OK)

class OrganisationRegistrationRequestRejectView(generics.UpdateAPIView):
    queryset = OrganisationRegistrationRequest.objects.all()
    serializer_class = OrganisationRegistrationRequestSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = OrganisationRegistrationRequest.REJECTED
        instance.save()
        instance.organisation.user.is_active = False  # Set is_active to False upon rejection
        instance.organisation.user.save()
        instance.send_rejection_email()
        return Response({'detail': 'Registration request rejected successfully.'}, status=status.HTTP_200_OK)


class OrganisationRegistrationView(generics.CreateAPIView):
    serializer_class = OrganisationRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the registration request
        organisation = serializer.save()
        registration_request = OrganisationRegistrationRequest.objects.create(organisation=organisation)

        # Check the approval status
        if registration_request.status == OrganisationRegistrationRequest.PENDING:
            return Response({'detail': 'Your account is yet to be approved by admin.'}, status=status.HTTP_200_OK)
        elif registration_request.status == OrganisationRegistrationRequest.REJECTED:
            return Response({'detail': 'Sorry, your request was denied by admin.'}, status=status.HTTP_400_BAD_REQUEST)

        # You can send an email or notification to the admin here

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class OrganisationProfileEditView(UpdateAPIView):
    serializer_class = OrganisationProfileEditSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class OrganisationListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_active=True, is_organisation=True)
    serializer_class = OrganisationListSerializer


class OrganisationInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the organization associated with the logged-in user
        organisation = Organisation.objects.get(user=request.user)
        
        # Serialize the organization information
        serializer = OrganisationSerializer(organisation)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
