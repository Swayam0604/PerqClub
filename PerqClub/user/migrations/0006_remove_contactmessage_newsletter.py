# Generated by Django 5.2.1 on 2025-07-29 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_contactmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactmessage',
            name='newsletter',
        ),
    ]
