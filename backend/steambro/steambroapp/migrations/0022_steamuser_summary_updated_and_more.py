# Generated by Django 4.0.4 on 2022-04-18 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steambroapp', '0021_remove_steamgame_background_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='steamuser',
            name='summary_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='steamuser',
            name='friendships_are_public',
            field=models.BooleanField(default=True),
        ),
    ]