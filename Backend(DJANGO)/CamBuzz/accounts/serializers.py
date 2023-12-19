from rest_framework import exceptions
from django.contrib.auth import authenticate

from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    is_student = serializers.BooleanField()
    is_organisation = serializers.BooleanField()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate(self, data):
        user = self.context['request'].user

        current_password = data.get("current_password")
        new_password = data.get("new_password")
        confirm_new_password = data.get("confirm_new_password")

        # Check if the current password is correct
        if not user.check_password(current_password):
            raise serializers.ValidationError("Current password is incorrect!")

        # Check if the new passwords match
        if new_password != confirm_new_password:
            raise serializers.ValidationError("New passwords do not match!")

        # Check if the new password is different from the current password
        if current_password == new_password:
            raise serializers.ValidationError("New password must be different from the current password!")

        return data
    

class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField()
