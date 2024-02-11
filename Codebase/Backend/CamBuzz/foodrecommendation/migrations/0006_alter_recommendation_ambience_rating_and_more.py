# Generated by Django 4.2.6 on 2023-11-13 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodrecommendation', '0005_alter_recommendation_ambience_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='ambience_rating',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='avg_user_rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='food_rating',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='service_rating',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]