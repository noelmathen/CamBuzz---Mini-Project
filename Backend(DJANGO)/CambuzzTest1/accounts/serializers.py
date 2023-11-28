from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import exceptions
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        max_length=50,  # Change the maximum length
        required=True,   # Make it required
    )
    last_name = serializers.CharField(
        max_length=100,  # Change the maximum length
        required=False,   # Make it required
    )
    email = serializers.CharField(
        max_length=200,  # Change the maximum length
        required=True,   # Make it required
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}   #won't be exposed in responses.

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        # Check if the email is already in use
        if User.objects.filter(email=email).exists():
            raise exceptions.ValidationError("Email is already in use.")

        # Check if the username is already in use
        if User.objects.filter(username=username).exists():
            raise exceptions.ValidationError("Username is already in use.")

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    raise exceptions.ValidationError("User is not active.")
            else:
                raise exceptions.ValidationError("Invalid username or password.")
        else:
            raise exceptions.ValidationError("Both username and password are required.")

        data['user'] = user
        return data

