# Generated by Django 4.2.6 on 2023-11-15 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodrecommendation', '0015_remove_restaurant_number_of_recommendations'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='number_of_recommendations',
            field=models.IntegerField(default=0),
        ),
    ]