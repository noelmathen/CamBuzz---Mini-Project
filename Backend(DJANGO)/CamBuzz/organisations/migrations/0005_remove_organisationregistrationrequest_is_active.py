# Generated by Django 4.2.7 on 2023-11-29 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0004_organisationregistrationrequest_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisationregistrationrequest',
            name='is_active',
        ),
    ]
