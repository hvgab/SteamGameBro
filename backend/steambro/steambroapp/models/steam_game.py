from django.db import models
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File

class SteamGame(models.Model):
    # Base App Info
    appid = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    
    # IMG
    icon_url = models.CharField(max_length=500, blank=True, null=True)
    icon = models.ImageField(upload_to='SteamGame', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    logo_url = models.CharField(max_length=500, blank=True, null=True)
    logo = models.ImageField(upload_to='SteamGame', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    header_url = models.CharField(max_length=500, blank=True, null=True)
    header = models.ImageField(upload_to='SteamGame', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    background_url = models.CharField(max_length=500, blank=True, null=True)
    background = models.ImageField(upload_to='SteamGame', height_field=None, width_field=None, max_length=None, blank=True, null=True)

    # Detailed App Info:
    has_detailed_info = models.BooleanField(default=False)
    detailed_description = models.TextField(blank=True, null=True)
    about_the_game = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)

    # Webapp fields
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __repr__(self):
        return f'<SteamGame({self.appid}, name={self.name!r})>'

    def __str__(self):
        return f'{self.name} ({self.appid})'

    # def save(self, *args, **kwargs):
    #     """Overwrite default save function."""
    #     self.get_remote_image()
    #     super(SteamGame, self).save(*args, **kwargs)

    def get_remote_image(self):
        IMG_ICON_URL = f'http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.icon_url}.jpg'
        IMG_LOGO_URL = f'http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.logo_url}.jpg'
        if self.icon_url and not self.icon:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(IMG_ICON_URL).read())
            img_temp.flush()
            self.icon.save(f'{self.appid}_icon', File(img_temp))

        if self.logo_url and not self.logo:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(IMG_LOGO_URL).read())
            img_temp.flush()
            self.logo.save(f'{self.appid}_logo', File(img_temp))

        # self.save()
