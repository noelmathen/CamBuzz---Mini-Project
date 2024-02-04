#student/serializers.py
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from .models import Student
from accounts.models import CustomUser
from django.contrib.auth import authenticate
from django.conf import settings

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



class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('joining_year', 'phone_number', 'photo', 'branch', 'division', 'gender',)


class UserProfileEditSerializer(serializers.ModelSerializer):
    student_data = StudentProfileSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'student_data')

    def update(self, instance, validated_data):
        # Extract student data if provided
        student_data = validated_data.pop('student_data', None)

        # Update CustomUser fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        # Update and save CustomUser
        instance.save()

        # Update Student fields if student_data is provided
        if student_data:
            student_instance, created = Student.objects.get_or_create(user=instance)

            # Update Student fields
            student_instance.joining_year = student_data.get('joining_year', student_instance.joining_year)
            student_instance.phone_number = student_data.get('phone_number', student_instance.phone_number)
            student_instance.photo = student_data.get('photo', student_instance.photo)

            student_instance.branch = student_data.get('branch', student_instance.branch)
            student_instance.division = student_data.get('division', student_instance.division)
            student_instance.gender = student_data.get('gender', student_instance.gender)

            # Automatically update passout_year if joining_year is provided
            if 'joining_year' in student_data:
                student_instance.passout_year = student_data['joining_year'] + 4

            # Save Student
            student_instance.save()

        return instance


class ProfileEditDataSerializer(serializers.ModelSerializer):
    # Include fields from the associated user model
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    batch = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('user', 'batch', 'branch', 'division', 'gender', 'phone_number', 'first_name', 'last_name', 'username', 'email', 'photo', )

    def get_username(self, obj):
        return obj.user.username
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name

    def get_email(self, obj):
        return obj.user.email
    
    def get_photo(self, obj):
        if obj.photo:
            return  'http://127.0.0.1:8000' + obj.photo.url
        return None
    
    def get_batch(self, obj):
        return f"{obj.joining_year} - {obj.passout_year}"



class StudentSerializer(serializers.ModelSerializer):
    # Include fields from the associated user model
    full_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    batch = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('user', 'batch', 'branch', 'division', 'gender', 'phone_number', 'full_name', 'username', 'email', 'photo', )

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email
    
    def get_photo(self, obj):
        if obj.photo:
            return  'http://127.0.0.1:8000' + obj.photo.url
        return None
    
    def get_batch(self, obj):
        return f"{obj.joining_year} - {obj.passout_year}"


