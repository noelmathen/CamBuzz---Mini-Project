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
    user_data = CustomUserRegistrationSerializer(required=False)

    class Meta:
        model = Organisation
        fields = ['about','website_link', 'linkedin_profile_link', 'instagram_username', 'facebook', 'photo', 'user_data']

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
    

class OrganisationProfileEditDataSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Organisation
        fields = ('user', 'about', 'website_link', 'linkedin_profile_link', 'instagram_username', 'facebook', 'first_name', 'last_name', 'username', 'email', 'photo')

    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email
    
    def get_photo(self, obj):
        if obj.photo:
            return  'http://127.0.0.1:8000' + obj.photo.url
        return None
 

class OrganisationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name']


class OrganisationSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Organisation
        fields = ('user', 'about', 'website_link', 'linkedin_profile_link', 'instagram_username', 'facebook','full_name', 'username', 'email', 'photo')

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

   