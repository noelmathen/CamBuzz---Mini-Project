# Generated by Django 4.2.6 on 2023-10-24 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiclepooling', '0002_alter_vehiclelisting_seats_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclelisting',
            name='vehicle_number',
            field=models.CharField(max_length=15),
        ),
    ]