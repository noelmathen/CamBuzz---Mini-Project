#foodrecommendation/serializers.py
from rest_framework import serializers
from .models import Restaurant, Recommendation
import random
from django.contrib.sites.shortcuts import get_current_site


class AddReviewFromMainPageSerializer(serializers.Serializer):
    restaurant_name = serializers.CharField(max_length=100)
    restaurant_location = serializers.CharField(max_length=100)
    food_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    service_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    ambience_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    avg_user_price_per_head = serializers.DecimalField(max_digits=6, decimal_places=2)
    top_recommendation = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000, required=False)
    image = serializers.ImageField(required=False)



class AddReviewFromRestaurantPageSerializer(serializers.Serializer):
    food_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    service_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    ambience_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    avg_user_price_per_head = serializers.DecimalField(max_digits=6, decimal_places=2)
    top_recommendation = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    image = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        # Your logic to update the recommendation instance
        instance.food_rating = validated_data.get('food_rating', instance.food_rating)
        instance.service_rating = validated_data.get('service_rating', instance.service_rating)
        instance.ambience_rating = validated_data.get('ambience_rating', instance.ambience_rating)
        instance.top_recommendation = validated_data.get('top_recommendation', instance.top_recommendation)
        instance.avg_user_price_per_head = validated_data.get('avg_user_price_per_head', instance.avg_user_price_per_head)
        instance.description = validated_data.get('description', instance.description)
        instance.ambience_rating = validated_data.get('ambience_rating', instance.ambience_rating)
        instance.save()

        # Update overall_price and overall_rating of the associated restaurant
        restaurant = instance.restaurant
        recommendations_for_restaurant = Recommendation.objects.filter(restaurant=restaurant)
        total_prices = sum([r.avg_user_price_per_head for r in recommendations_for_restaurant])
        total_ratings = sum([r.avg_user_rating for r in recommendations_for_restaurant])

        # Calculate new overall_price and overall_rating
        restaurant.overall_price = total_prices / len(recommendations_for_restaurant)
        restaurant.overall_rating = total_ratings / len(recommendations_for_restaurant)
        restaurant.save()
        return instance



class ListTopRatedRestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location', 'overall_rating', 'overall_price', 'image', 'number_of_recommendations']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Retrieve all recommendations for the current restaurant
        recommendations = instance.recommendation_set.all()

        # Check if there are any recommendations with images
        recommendations_with_images = [rec for rec in recommendations if rec.image]

        if recommendations_with_images:
            # Randomly select an image from recommendations
            random_recommendation = random.choice(recommendations_with_images)
            representation['image'] = 'http://127.0.0.1:8000/'+random_recommendation.image.url
        else:
            representation['image'] = None

        return representation



class RecommendationDetailSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    profile_picture = serializers.SerializerMethodField()
    full_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Recommendation
        fields = (
            'user_name',
            'profile_picture',
            'food_rating',
            'service_rating',
            'ambience_rating',
            'avg_user_rating',
            'avg_user_price_per_head',
            'top_recommendation',
            'description',
            'full_image_url',  # Include the full image URL in the response
        )

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        user = obj.user
        profile_picture_url = None

        # Check if the user has a profile picture
        if hasattr(user, 'student_profile') and user.student_profile.photo:
            profile_picture_url = 'http://127.0.0.1:8000'+(user.student_profile.photo.url)
        elif user.profile_picture:
            profile_picture_url = 'http://127.0.0.1:8000'+(user.profile_picture.url)

        return profile_picture_url

    def get_full_image_url(self, obj):
        try:
            if(obj.image):
                print(obj.image)
                full_image_url = 'http://127.0.0.1:8000' + obj.image.url
                print(full_image_url)
            else:
                return
        except AttributeError:  # Handle cases where 'image' might not be present
            full_image_url = 'http://127.0.0.1:8000/media/restaurant_images/default_rest_img.jpg'  # Or use a placeholder image URL here
        return full_image_url



class RestaurantDetailSerializer(serializers.ModelSerializer):
    recommendations = RecommendationDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = (
            'name',
            'location',
            'overall_price',
            'overall_rating',
            'number_of_recommendations',
            'recommendations',
        )



class YourFoodRecommendationsSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    restaurant_location = serializers.CharField(source='restaurant.location', read_only=True)
    user_name = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = Recommendation
        fields = (
            'id',
            'user_name',
            'restaurant_id',
            'restaurant_name',
            'restaurant_location',
            'food_rating',
            'service_rating',
            'ambience_rating',
            'avg_user_rating',
            'avg_user_price_per_head',
            'top_recommendation',
            'description',
            'image',
        )



class EditReviewSerialzier(serializers.Serializer):
    food_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    service_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    ambience_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    avg_user_price_per_head = serializers.DecimalField(max_digits=6, decimal_places=2)
    top_recommendation = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    image = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        # Your logic to update the recommendation instance
        instance.food_rating = validated_data.get('food_rating', instance.food_rating)
        instance.service_rating = validated_data.get('service_rating', instance.service_rating)
        instance.ambience_rating = validated_data.get('ambience_rating', instance.ambience_rating)
        instance.top_recommendation = validated_data.get('top_recommendation', instance.top_recommendation)
        instance.avg_user_price_per_head = validated_data.get('avg_user_price_per_head', instance.avg_user_price_per_head)
        instance.description = validated_data.get('description', instance.description)
        instance.ambience_rating = validated_data.get('ambience_rating', instance.ambience_rating)
        
        # Check if a new image is provided
        new_image = validated_data.get('image', None)
        if new_image:
            instance.image = new_image

        instance.save()
        
        instance.save()

        # Update overall_price and overall_rating of the associated restaurant
        restaurant = instance.restaurant
        recommendations_for_restaurant = Recommendation.objects.filter(restaurant=restaurant)
        total_prices = sum([r.avg_user_price_per_head for r in recommendations_for_restaurant])
        total_ratings = sum([r.avg_user_rating for r in recommendations_for_restaurant])

        # Calculate new overall_price and overall_rating
        restaurant.overall_price = total_prices / len(recommendations_for_restaurant)
        restaurant.overall_rating = total_ratings / len(recommendations_for_restaurant)
        restaurant.save()
        return instance



class DeleteReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = Recommendation
        fields = (
            'user_name',  # Change this to user_name
            'profile_picture',
            'food_rating',
            'service_rating',
            'ambience_rating',
            'avg_user_rating',
            'avg_user_price_per_head',
            'top_recommendation',
            'description',
            'full_image_url',
        )
