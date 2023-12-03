#student/serializers.py
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from .models import Student
from accounts.models import CustomUser
from django.contrib.auth import authenticate

class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('joining_year', 'branch', 'division', 'phone_number', 'gender', 'photo')

class UserRegistrationSerializer(serializers.ModelSerializer):
    student_data = StudentRegistrationSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'student_data')

    def create(self, validated_data):
        # Extract student data if provided
        student_data = validated_data.pop('student_data', None)

        # Hash the password
        validated_data['password'] = make_password(validated_data['password'])

        # Create CustomUser
        custom_user = CustomUser.objects.create(**validated_data)

        # If student data is provided, create Student and link it to CustomUser
        if student_data:
            # Set the user field of the Student model
            student_data['user'] = custom_user

            # Manually set the passout_year based on the joining_year
            joining_year = student_data.get('joining_year')
            if joining_year:
                student_data['passout_year'] = joining_year + 4

            # Create the student
            Student.objects.create(**student_data)

        return custom_user




# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'email', 'username', 'password')


# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ('joining_year', 'branch', 'division', 'phone_number', 'gender', 'photo')




# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, data):
#         username = data.get("username")
#         password = data.get("password")

#         if username and password:
#             user = authenticate(username=username, password=password)
#             if user:
#                 if user.is_active:
#                     data["user"] = user
#                 else:
#                     raise serializers.ValidationError("User is not active.")
#             else:
#                 raise serializers.ValidationError("Incorrect username or password.")
#         else:
#             raise serializers.ValidationError("Both username and password are required.")

#         return data
    

# class UserProfileUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'phone_number', 'username', 'branch', 'division', 'gender', 'photo')


# class ChangePasswordSerializer(serializers.Serializer):
#     current_password = serializers.CharField()
#     new_password = serializers.CharField()
#     confirm_new_password = serializers.CharField()

#     def validate(self, data):
#         user = self.context['request'].user

#         current_password = data.get("current_password")
#         new_password = data.get("new_password")
#         confirm_new_password = data.get("confirm_new_password")

#         # Check if the current password is correct
#         if not check_password(current_password, user.password):
#             raise serializers.ValidationError("Current password is incorrect!")

#         # Check if the new passwords match
#         if new_password != confirm_new_password:
#             raise serializers.ValidationError("New passwords do not match!")

#         # Check if the new password is different from the current password
#         if current_password == new_password:
#             raise serializers.ValidationError("New password must be different from the current password!")

#         return data
    

# class DeleteAccountSerializer(serializers.Serializer):
#     password = serializers.CharField()
