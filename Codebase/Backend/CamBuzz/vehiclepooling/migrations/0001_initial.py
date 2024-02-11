# Generated by Django 4.2.6 on 2023-10-24 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_location', models.CharField(max_length=100)),
                ('to_location', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField()),
                ('eta', models.DateTimeField()),
                ('vehicle_type', models.CharField(choices=[('Car', 'Car'), ('Bike', 'Bike'), ('Scooty', 'Scooty')], max_length=10)),
                ('extra_helmet', models.BooleanField(default=False)),
                ('vehicle_number', models.CharField(max_length=10)),
                ('seats_available', models.PositiveSmallIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('description', models.CharField(max_length=1000)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]