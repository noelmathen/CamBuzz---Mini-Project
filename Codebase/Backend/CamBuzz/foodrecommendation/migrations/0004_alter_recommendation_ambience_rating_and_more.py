# Generated by Django 4.2.6 on 2023-11-12 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodrecommendation', '0003_alter_recommendation_ambience_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='ambience_rating',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='avg_user_price_per_head',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='avg_user_rating',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='food_rating',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='service_rating',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]