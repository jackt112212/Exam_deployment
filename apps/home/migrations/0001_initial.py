# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-22 20:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Traveler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=45)),
                ('l_name', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=45)),
                ('plan', models.TextField(null=True)),
                ('startdate', models.DateField()),
                ('enddate', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('followers', models.ManyToManyField(related_name='group_trips', to='home.Traveler')),
                ('planner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_trips', to='home.Traveler')),
            ],
        ),
    ]
