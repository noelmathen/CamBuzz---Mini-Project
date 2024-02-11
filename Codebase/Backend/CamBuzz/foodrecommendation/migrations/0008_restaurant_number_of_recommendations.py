# Generated by Django 4.2.6 on 2023-11-14 14:06

from django.db import migrations, models

# def update_number_of_recommendations(apps, schema_editor):
#     Restaurant = apps.get_model('foodrecommendation', 'Restaurant')

#     for restaurant in Restaurant.objects.all():
#         restaurant.number_of_recommendations = restaurant.recommendation_set.count()
#         restaurant.save()

class Migration(migrations.Migration):

    dependencies = [
        ('foodrecommendation', '0007_alter_restaurant_overall_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='number_of_recommendations',
            field=models.IntegerField(default=0),
        ),
    ]