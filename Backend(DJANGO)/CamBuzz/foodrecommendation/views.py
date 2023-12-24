#foodrecommendation/views.py
from rest_framework import viewsets
from .models import Restaurant, Recommendation
from .serializers import AddReviewFromMainPageSerializer, AddReviewFromRestaurantPageSerializer, ListTopRatedRestaurantsSerializer, RecommendationDetailSerializer, RestaurantDetailSerializer, YourFoodRecommendationsSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.generics import RetrieveAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly

class AddReviewFromMainPage(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = AddReviewFromMainPageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        restaurant_name = serializer.validated_data.get('restaurant_name')
        restaurant_location = serializer.validated_data.get('restaurant_location')
        food_rating = serializer.validated_data.get('food_rating')
        service_rating = serializer.validated_data.get('service_rating')
        ambience_rating = serializer.validated_data.get('ambience_rating')
        avg_user_price_per_head = serializer.validated_data.get('avg_user_price_per_head')
        top_recommendation = serializer.validated_data.get('top_recommendation')
        description = serializer.validated_data.get('description')
        image = serializer.validated_data.get('image')

        restaurant = None

        # Use select_for_update to lock the row during the check and creation process
        with transaction.atomic():
            # Check if the user has already made a recommendation for the same restaurant
            
            existing_recommendation = Recommendation.objects.filter(
                user=request.user,
                restaurant__name=restaurant_name,
                restaurant__location=restaurant_location,
            ).first()

            if existing_recommendation:
                return Response(
                    {"message": "You have already made a recommendation for this restaurant."},
                    status=status.HTTP_400_BAD_REQUEST
                )
    

            # Check if the restaurant already exists; if not, create it
            restaurant, created = Restaurant.objects.get_or_create(
                name=restaurant_name,
                location=restaurant_location,
                defaults={'overall_price': 0, 'overall_rating': 0, 'number_of_recommendations': 0},
            )
            restaurant.save()
            restaurant.refresh_from_db()

            # Create or update the recommendation
            recommendation, recommendation_created = Recommendation.objects.update_or_create(
                user=request.user,
                restaurant=restaurant,
                defaults={
                    'food_rating': food_rating,
                    'service_rating': service_rating,
                    'ambience_rating': ambience_rating,
                    'avg_user_price_per_head': avg_user_price_per_head,
                    'top_recommendation': top_recommendation,
                    'description': description,
                    'image': image,
                }
            )

            if not recommendation_created:
                # Recommendation already existed, update its fields
                recommendation.food_rating = food_rating
                recommendation.service_rating = service_rating
                recommendation.ambience_rating = ambience_rating
                recommendation.avg_user_price_per_head = avg_user_price_per_head
                recommendation.top_recommendation = top_recommendation
                recommendation.description = description
                recommendation.image = image
                recommendation.save()

            # Update overall_price and overall_rating of the restaurant
            recommendations_for_restaurant = Recommendation.objects.filter(restaurant=restaurant)
            total_prices = sum([r.avg_user_price_per_head for r in recommendations_for_restaurant])
            total_ratings = sum([r.avg_user_rating for r in recommendations_for_restaurant])

            # Calculate new overall_price and overall_rating
            restaurant.overall_price = total_prices / len(recommendations_for_restaurant)
            restaurant.overall_rating = total_ratings / len(recommendations_for_restaurant)
            restaurant.save()

            restaurant.number_of_recommendations = Recommendation.objects.filter(restaurant=restaurant).count()
            restaurant.save()

            first_name = request.user.first_name
            user_id = request.user.id
            if created:
                success_message = f"{first_name}(user_id:{user_id}) successfully created a recommendation for {restaurant.name}, {restaurant.location}(restaurant_id:{restaurant.id}). Also, {first_name} is the first one to add a review/ recommendation for this restaurant!" 
            else:
                success_message = f"{first_name}(user_id:{user_id}) successfully created a recommendation for {restaurant.name}, {restaurant.location}(restaurant_id:{restaurant.id})" 
            return Response({"message": success_message},status=status.HTTP_201_CREATED)


class AddReviewForRestaurant(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, restaurant_id, *args, **kwargs):
        # Ensure that the restaurant with the given ID exists
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        # Check if the user has already made a recommendation for this restaurant
        existing_recommendation = Recommendation.objects.filter(
            user=request.user,
            restaurant=restaurant,
        ).first()

        if existing_recommendation:
            return Response(
                {"message": "You have already made a recommendation for this restaurant."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AddReviewFromRestaurantPageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract data from the validated serializer
        food_rating = serializer.validated_data.get('food_rating')
        service_rating = serializer.validated_data.get('service_rating')
        ambience_rating = serializer.validated_data.get('ambience_rating')
        avg_user_price_per_head = serializer.validated_data.get('avg_user_price_per_head')
        top_recommendation = serializer.validated_data.get('top_recommendation')
        description = serializer.validated_data.get('description')
        image = serializer.validated_data.get('image')

        # Create or update the recommendation for the restaurant and user
        recommendation, created = Recommendation.objects.update_or_create(
            user=request.user,
            restaurant=restaurant,
            defaults={
                'food_rating': food_rating,
                'service_rating': service_rating,
                'ambience_rating': ambience_rating,
                'avg_user_price_per_head': avg_user_price_per_head,
                'top_recommendation': top_recommendation,
                'description': description,
                'image': image,
            }
        )

        if not created:
            # Recommendation already existed, update its fields
            recommendation.food_rating = food_rating
            recommendation.service_rating = service_rating
            recommendation.ambience_rating = ambience_rating
            recommendation.avg_user_price_per_head = avg_user_price_per_head
            recommendation.top_recommendation = top_recommendation
            recommendation.description = description
            recommendation.image = image
            recommendation.save()

        # Update overall_price and overall_rating of the restaurant
        recommendations_for_restaurant = Recommendation.objects.filter(restaurant=restaurant)
        total_prices = sum([r.avg_user_price_per_head for r in recommendations_for_restaurant])
        total_ratings = sum([r.avg_user_rating for r in recommendations_for_restaurant])

        # Calculate new overall_price and overall_rating
        restaurant.overall_price = total_prices / len(recommendations_for_restaurant)
        restaurant.overall_rating = total_ratings / len(recommendations_for_restaurant)
        restaurant.save()

        # Update the number_of_recommendations
        restaurant.number_of_recommendations = recommendations_for_restaurant.count()
        restaurant.save()

        first_name = request.user.first_name
        user_id = request.user.id
        success_message = f"{first_name}(user_id:{user_id}) successfully created a recommendation for {restaurant.name}, {restaurant.location}(restaurant_id:{restaurant.id})" 
        return Response({"message": success_message},status=status.HTTP_201_CREATED)


class ListTopRatedRestaurants(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve optional query parameters
        name = request.query_params.get('name')
        location = request.query_params.get('location')
        overall_price = request.query_params.get('overall_price')

        # Filter restaurants based on optional parameters
        filtered_restaurants = Restaurant.objects.annotate(num_recommendations=Count('recommendation')).order_by('-overall_rating')
        if name:
            filtered_restaurants = filtered_restaurants.filter(name__icontains=name)
        if location:
            filtered_restaurants = filtered_restaurants.filter(location__icontains=location)
        if overall_price:
            filtered_restaurants = filtered_restaurants.filter(overall_price__lte=overall_price)

        # Order the filtered restaurants by overall_rating in descending order
        ordered_restaurants = filtered_restaurants.order_by('-overall_rating')

        if not ordered_restaurants.exists():
            return Response({"message": "No restaurants are suggested."}, status=status.HTTP_200_OK)

        # Serialize and return the ordered restaurants
        serializer = ListTopRatedRestaurantsSerializer(ordered_restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RestaurantDetailView(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Retrieve the list of recommendations for the restaurant
        recommendations = Recommendation.objects.filter(restaurant=instance)
        recommendation_serializer = RecommendationDetailSerializer(recommendations, many=True)

        # Combine restaurant details and recommendations in the response
        response_data = {
            'restaurant_details': self.get_serializer(instance).data,
            'recommendations': recommendation_serializer.data
        }

        return Response(response_data)


class YourFoodRecommendationsView(ListAPIView):
    serializer_class = YourFoodRecommendationsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Retrieve recommendations made by the authenticated user
        return Recommendation.objects.filter(user=self.request.user).order_by('-avg_user_rating')


class EditRecommendationView(RetrieveUpdateAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = AddReviewFromRestaurantPageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        first_name = request.user.first_name
        message = f"{first_name}'s food recommendation updation was successfull"
        return Response(data={'message':message,'data':serializer.data }, status=status.HTTP_200_OK)
    

class DeleteRecommendationView(RetrieveDestroyAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        restaurant = instance.restaurant

        # Perform the recommendation deletion
        self.perform_destroy(instance)

        # Update the number_of_recommendations field in the Restaurant table
        restaurant.number_of_recommendations = Recommendation.objects.filter(restaurant=restaurant).count()
        restaurant.save()

        # Check if the restaurant should be deleted
        recommendations_for_restaurant = Recommendation.objects.filter(restaurant=restaurant)
        first_name = request.user.first_name
        if recommendations_for_restaurant.count() == 0:
            restaurant_name = restaurant.name
            restaurant.delete()
            message = f"The last recommendation for {restaurant_name} has been deleted by {first_name}, and the restaurant({restaurant_name}) is removed."
        else:
            message = f"Recommendation deleted successfully by {first_name}"

        return Response({"detail": message}, status=status.HTTP_204_NO_CONTENT)



