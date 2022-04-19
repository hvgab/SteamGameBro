from django.db import models
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File
import requests
import logging

logger = logging.getLogger(__name__)

class SteamGame(models.Model):
    # Base App Info
    steam_id = models.PositiveIntegerField(unique=True)
    steam_id_64 = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=32, blank=True, null=True)
    headline = models.CharField(max_length=32, blank=True, null=True)
    summary = models.CharField(max_length=32, blank=True, null=True)
    avatar_icon = models.CharField(max_length=32, blank=True, null=True)
    avatar_medium = models.CharField(max_length=32, blank=True, null=True)
    avatar_full = models.CharField(max_length=32, blank=True, null=True)
    

    def __repr__(self):
        return f'<SteamGroup({self.id}, name={self.name!r})>'

    def __str__(self):
        return f'{self.name} ({self.id})'

    