# Generated by Django 4.2.7 on 2024-01-02 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodrecommendation', '0019_alter_recommendation_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
