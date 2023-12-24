#foodrecommendation/models.py
from django.db import models
from student.models import Student, CustomUser
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.db.models import Count

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    overall_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    overall_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    image = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)
    number_of_recommendations = models.IntegerField(default=0)


    def calculate_overall_rating(self):
        recommendations = self.recommendation_set.all()
        if recommendations:
            total_ratings = sum([r.avg_user_rating for r in recommendations])
            return total_ratings / len(recommendations)
        return 0

    def calculate_overall_price(self):
        recommendations = self.recommendation_set.all()
        if recommendations:
            total_prices = sum([r.avg_user_price_per_head for r in recommendations])
            return total_prices / len(recommendations)
        return 0

    def __str__(self):
        return f"{self.name} - {self.location}"    


class Recommendation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    food_rating = models.DecimalField(max_digits=2, decimal_places=1)
    service_rating = models.DecimalField(max_digits=2, decimal_places=1)
    ambience_rating = models.DecimalField(max_digits=2, decimal_places=1)
    top_recommendation = models.CharField(max_length=100)
    description = models.TextField()
    # Fields for calculated values
    avg_user_rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    avg_user_price_per_head = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)

    @property
    def calculate_avg_user_rating(self):
        return (self.food_rating + self.service_rating + self.ambience_rating) / 3
    
    def __str__(self):
        return f"{self.user.first_name}'s recommendation for {self.restaurant.name}"    
    


@receiver(pre_save, sender=Recommendation)
def calculate_avg_user_rating(sender, instance, **kwargs):
    instance.avg_user_rating = instance.calculate_avg_user_rating
pre_save.connect(calculate_avg_user_rating, sender=Recommendation)


@receiver(post_delete, sender=Recommendation)
def update_restaurant_stats(sender, instance, **kwargs):
    restaurant = instance.restaurant

    # Update total_prices and total_ratings
    recommendations_for_restaurant = Recommendation.objects.filter(restaurant=restaurant)
    if recommendations_for_restaurant:
        restaurant.total_prices = sum([r.avg_user_price_per_head for r in recommendations_for_restaurant])
        restaurant.total_ratings = sum([r.avg_user_rating for r in recommendations_for_restaurant])
        restaurant.overall_price = restaurant.total_prices / len(recommendations_for_restaurant)
        restaurant.overall_rating = restaurant.total_ratings / len(recommendations_for_restaurant)

    restaurant.save()
post_delete.connect(update_restaurant_stats, sender=Recommendation)



