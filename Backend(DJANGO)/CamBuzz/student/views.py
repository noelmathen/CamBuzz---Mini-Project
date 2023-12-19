#student/views.py
from rest_framework import status, generics
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import CustomUser
from student.models import Student
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    UserRegistrationSerializer,
    UserProfileEditSerializer,
)

class StudentRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # Automatically calculate passout year
            joining_year = serializer.validated_data.get('student_data', {}).get('joining_year')
            if joining_year:
                serializer.validated_data['student_data']['passout_year'] = joining_year + 4

            # Set the role for the user (assuming 'is_student' is a valid field in CustomUser)
            serializer.validated_data['is_student'] = True

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StudentProfileEditView(UpdateAPIView):
    serializer_class = UserProfileEditSerializer
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

