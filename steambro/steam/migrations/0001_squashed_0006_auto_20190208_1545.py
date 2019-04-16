# Generated by Django 2.1.5 on 2019-04-16 13:40

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    replaces = [('steam', '0001_initial'), ('steam', '0002_auto_20190204_1608'), ('steam', '0003_auto_20190204_1719'), ('steam', '0004_auto_20190204_2218'), ('steam', '0005_auto_20190204_2231'), ('steam', '0006_auto_20190208_1545')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SteamUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('steamid', models.BigIntegerField()),
                ('personaname', models.CharField(max_length=255)),
                ('profileurl', models.CharField(max_length=500)),
                ('avatar', models.CharField(max_length=500)),
                ('avatarmedium', models.CharField(max_length=500)),
                ('avatarfull', models.CharField(max_length=500)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('ownedGames', models.CharField(blank=True, max_length=1000000, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('friends', models.ManyToManyField(to='steam.SteamUser')),
            ],
        ),
        migrations.CreateModel(
            name='SteamGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appid', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('img_icon_url', models.CharField(max_length=500)),
                ('img_icon', models.ImageField(upload_to='SteamGame')),
                ('img_logo_url', models.CharField(max_length=500)),
                ('img_logo', models.ImageField(upload_to='SteamGame')),
                ('has_detailed_info', models.BooleanField(default=False)),
            ],
        ),
    ]
