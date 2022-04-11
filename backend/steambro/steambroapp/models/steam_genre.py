from django.db import models
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File

class SteamGenre(models.Model):
    description = models.CharField(max_length=255)
    
    def __repr__(self):
        return f'<SteamGenre({self.id}, description={self.description!r})>'

    def __str__(self):
        return f'{self.description}'