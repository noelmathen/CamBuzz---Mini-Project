# organisations/serializers.py
from rest_framework import serializers
from .models import OrganisationRegistrationRequest, Organisation
from accounts.models import CustomUser

class OrganisationRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationRegistrationRequest
        fields = '__all__'

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'email', 'username', 'password']



class OrganisationRegistrationSerializer(serializers.ModelSerializer):
    user_data = CustomUserRegistrationSerializer()

    class Meta:
        model = Organisation
        fields = ['photo', 'about','website_link', 'linkedin_profile_link', 'instagram_username', 'facebook', 'user_data']

    def create(self, validated_data):
        user_data = validated_data.pop('user_data', None)
        password = user_data.pop('password', None)

        # Create CustomUser
        user = CustomUser.objects.create_organisation_user(**user_data)
        if password:
            user.set_password(password)
        user.save()

        # Create Organisation
        organisation = Organisation.objects.create(user=user, **validated_data)

        return organisation
 
