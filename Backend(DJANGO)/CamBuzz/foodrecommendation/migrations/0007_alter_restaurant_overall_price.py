# Generated by Django 4.2.6 on 2023-11-13 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodrecommendation', '0006_alter_recommendation_ambience_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='overall_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
