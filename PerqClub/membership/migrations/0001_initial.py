# Generated by Django 5.2.1 on 2025-06-19 07:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('PerkPlus', 'PerkPlus'), ('PerkElite', 'PerkElite'), ('PerkSupreme', 'PerkSupreme')], max_length=50, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('description', models.TextField()),
                ('is_most_popular', models.BooleanField(default=False)),
                ('perks', models.TextField(blank=True, help_text='Perks separated by newlines')),
            ],
        ),
        migrations.CreateModel(
            name='PlanFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_text', models.CharField(max_length=255)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='membership.membershipplan')),
            ],
            options={
                'unique_together': {('feature_text', 'plan')},
            },
        ),
    ]
