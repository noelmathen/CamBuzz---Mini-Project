# Generated by Django 4.2.7 on 2023-12-02 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customusertoken'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUserToken',
        ),
    ]
