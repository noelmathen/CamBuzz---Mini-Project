# Generated by Django 4.2.6 on 2023-11-15 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodrecommendation', '0010_alter_recommendation_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodrecommendation.restaurant'),
        ),
    ]
