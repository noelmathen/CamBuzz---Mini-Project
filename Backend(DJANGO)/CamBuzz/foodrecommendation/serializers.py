from rest_framework import serializers
from .models import Restaurant, Recommendation


class AddReviewFromMainPageSerializer(serializers.Serializer):
    restaurant_name = serializers.CharField(max_length=100)
    restaurant_location = serializers.CharField(max_length=100)
    food_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    service_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    ambience_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    avg_user_price_per_head = serializers.DecimalField(max_digits=6, decimal_places=2)
    top_recommendation = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
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


class RecommendationDetailSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Recommendation
        fields = (
            'user_name',
            'food_rating',
            'service_rating',
            'ambience_rating',
            'avg_user_rating',
            'avg_user_price_per_head',
            'top_recommendation',
            'description',
            'image',
        )


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



