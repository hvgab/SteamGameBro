from django.db import models
from .. import services
from ..models import SteamUser

class SteamUserManager(models.Manager):
    from steambroapp import service
    def get_or_api(self, steamid):
        try:
            return super().get_queryset().get(steamid=steamid)
        except SteamUser.ObjectDoesNotExist:
            steam_user = services.refresh_steam_user_summary(steamid=steamid)
            return steam_user