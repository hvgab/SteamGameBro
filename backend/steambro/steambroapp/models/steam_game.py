from django.db import models
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File
import requests
import logging

logger = logging.getLogger(__name__)

class SteamGame(models.Model):
    # Base App Info
    appid = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=32, blank=True, null=True)
    
    # IMG
    icon_url = models.CharField(max_length=500, blank=True, null=True)
    icon = models.ImageField(upload_to='SteamGame', height_field=None, width_field=None, max_length=None, blank=True, null=True)

    # Detailed App Info:
    has_detailed_info = models.BooleanField(default=False)
    detailed_description = models.TextField(blank=True, null=True)
    about_the_game = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)

    # website = models.URLField(blank=True, null=True)

    # Webapp fields
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __repr__(self):
        return f'<SteamGame({self.appid}, name={self.name!r})>'

    def __str__(self):
        return f'{self.name} ({self.appid})'

    def get_api_info(self):
        url = "https://store.steampowered.com/api/appdetails"
        params = {
            'appids':self.appid,
            'l':'english',
        }
        r = requests.get(url, params=params)
        try:
            rj = r.json()
        except Exception as e:
            logger.error('request error. \n{r.test}')
            return None

        rj_keys = rj.keys()
        root_key = list(rj_keys)[0]

        logger.debug(rj[root_key]['success'])
        if rj[root_key]['success'] == False:
            return None

        return rj[root_key]['data']


    def get_icon_url(self):
        return f'http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.icon_url}.jpg'

    @property
    def logo(self):
        # return f'http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.logo_url}.jpg'
        return f'https://steamcdn-a.akamaihd.net/steam/apps/{self.appid}/logo.png'

    @property
    def header(self):
        return f'https://steamcdn-a.akamaihd.net/steam/apps/{self.appid}/header.jpg'

    @property
    def library_hero(self):
        return f'https://steamcdn-a.akamaihd.net/steam/apps/{self.appid}/library_hero.jpg'

    @property
    def capsule(self):
        return f'https://steamcdn-a.akamaihd.net/steam/apps/{self.appid}/library_600x900.jpg'

    @property
    def hero_capsule(self):
        return f'https://cdn.cloudflare.steamstatic.com/steam/apps/{self.appid}/hero_capsule.jpg'

    @property
    def capsule_231x87(self):
        return f'https://cdn.cloudflare.steamstatic.com/steam/apps/{self.appid}/capsule_231x87.jpg'

    @property
    def capsule_467x181(self):
        return f'https://cdn.cloudflare.steamstatic.com/steam/apps/{self.appid}/capsule_467x181.jpg'

    @property
    def capsule_616x353(self):
        return f'https://cdn.cloudflare.steamstatic.com/steam/apps/{self.appid}/capsule_616x353.jpg'

    @property
    def capsule_big(self):
        return f'https://steamcdn-a.akamaihd.net/steam/apps/{self.appid}/library_600x900_2x.jpg'

    @property
    def page_background_generated(self):
        return f'https://steamcdn-a.akamaihd.net/steam/apps/{self.appid}/page_bg_generated.jpg'

    @property
    def page_background_raw(self):
        return f'https://cdn.cloudflare.steamstatic.com/steam/apps/{self.appid}/page_bg_raw.jpg'

    @property
    def page_background_generated_big_picture(self):
        return f'https://steamcdn-a.akamaihd.net/steam/apps/{self.appid}/page_bg_generated_v6b.jpg'

    @property
    def steam_store(self):
        return f'https://store.steampowered.com/app/{self.appid}/'

    

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
