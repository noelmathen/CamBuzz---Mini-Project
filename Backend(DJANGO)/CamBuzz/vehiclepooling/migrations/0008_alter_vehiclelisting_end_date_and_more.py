# Generated by Django 4.2.7 on 2023-12-20 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiclepooling', '0007_alter_vehiclelisting_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclelisting',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehiclelisting',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehiclelisting',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehiclelisting',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]