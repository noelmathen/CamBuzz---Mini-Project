# organisations/serializers.py
from rest_framework import serializers
from .models import OrganisationRegistrationRequest, Organisation

class OrganisationRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationRegistrationRequest
        fields = '__all__'


class OrganisationRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['name', 'photo', 'about', 'email', 'website_link', 'linkedin_profile_link', 'instagram_username', 'facebook', 'username', 'password']

