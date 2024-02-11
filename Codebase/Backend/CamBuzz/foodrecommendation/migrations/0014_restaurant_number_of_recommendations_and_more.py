# Generated by Django 4.2.6 on 2023-11-15 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodrecommendation', '0013_remove_restaurant_number_of_recommendations'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='number_of_recommendations',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodrecommendation.restaurant'),
        ),
    ]