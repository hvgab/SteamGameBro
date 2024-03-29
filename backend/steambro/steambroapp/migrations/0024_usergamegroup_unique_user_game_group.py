# Generated by Django 4.0.4 on 2022-04-20 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steambroapp', '0023_friendship_unique_friendship'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='usergamegroup',
            constraint=models.UniqueConstraint(fields=('user', 'game', 'group'), name='unique_user_game_group'),
        ),
    ]
