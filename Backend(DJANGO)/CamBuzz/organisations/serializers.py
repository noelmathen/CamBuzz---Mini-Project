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
 


class OrganisationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('about', 'website_link', 'instagram_username', 'facebook', 'photo')

class OrganisationProfileEditSerializer(serializers.ModelSerializer):
    user_data = OrganisationProfileSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', 'username', 'user_data')

    def update(self, instance, validated_data):
        # Extract organization data if provided
        user_data = validated_data.pop('user_data', None)

        # Update CustomUser fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.email = validated_data.get('email', instance.email)

        # Check if the username is changing
        new_username = validated_data.get('username', instance.username)
        if new_username != instance.username:
            # If changing, check if the new username is unique
            if CustomUser.objects.filter(username=new_username).exists():
                raise serializers.ValidationError("A user with that username already exists.")

        # Update and save CustomUser
        instance.username = new_username
        instance.save()

        # Update Organization fields if user_data is provided
        if user_data:
            organization_instance, created = Organisation.objects.get_or_create(user=instance)

            # Update Organization fields
            organization_instance.about = user_data.get('about', organization_instance.about)
            organization_instance.website_link = user_data.get('website_link', organization_instance.website_link)
            organization_instance.linkedin_profile_link = user_data.get('linkedin_profile_link', organization_instance.linkedin_profile_link)
            organization_instance.instagram_username = user_data.get('instagram_username', organization_instance.instagram_username)
            organization_instance.facebook = user_data.get('facebook', organization_instance.facebook)
            organization_instance.photo = user_data.get('photo', organization_instance.photo)

            # Save Organization
            organization_instance.save()

        return instance
    

