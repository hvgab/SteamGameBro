from django.db import models
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File

class GameGroup(models.Model):
    name = models.CharField(max_length=255)
    is_system_group = models.BooleanField(help_text="If this group is one of the defaults")
    
    def __repr__(self):
        return f'<GameGroup({self.id}, name={self.name!r})>'

    def __str__(self):
        return f'{self.name}'

