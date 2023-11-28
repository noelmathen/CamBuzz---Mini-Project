from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AddReviewFromMainPage, AddReviewForRestaurant, ListTopRatedRestaurants, RestaurantDetailView, YourFoodRecommendationsView, EditRecommendationView, DeleteRecommendationView

urlpatterns = [
    # path('', include(router.urls)),
    path('addreviewfrommainpage/', AddReviewFromMainPage.as_view(), name='add-review-from-main-page'),
    path('restaurants/<int:restaurant_id>/add_review/', AddReviewForRestaurant.as_view(), name='add_review_for_restaurant'),
    path('list_top_rated_restaurants/', ListTopRatedRestaurants.as_view(), name='list_top_rated_restaurants'),
    path('restaurants/<int:id>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('your_food_recommendations/', YourFoodRecommendationsView.as_view(), name='your-food-recommendations'),
    path('edit_recommendation/<int:pk>/', EditRecommendationView.as_view(), name='edit-recommendation'),
    path('delete_recommendation/<int:pk>/', DeleteRecommendationView.as_view(), name='delete_recommendation'),
]


