# Generated by Django 4.2.6 on 2023-11-15 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodrecommendation', '0011_alter_recommendation_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='number_of_recommendations',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]