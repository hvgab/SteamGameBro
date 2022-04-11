from django.core.management.base import BaseCommand, CommandError
from steambroapp.models import steam_game
from steambroapp.models import SteamUser, SteamGame
from time import sleep
import datetime as dt
from django.utils import timezone
import logging
from steambroapp.utils import sync_player
from ... import services

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Refresh Steam Game Details'

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int)
        parser.add_argument('--steam-appid', type=int)

    def handle(self, *args, **kwargs):

        if 'id' in kwargs and kwargs['id'] is not None:
            steam_game = SteamGame.objects.get(pk=kwargs['id'])
        elif 'steam_appid' in kwargs and kwargs['steam_appid'] is not None:
            steam_game = SteamGame.objects.get(appid=kwargs['steam_appid'])
        else:
            raise CommandError('Command must be run with either `--id` or `steam-appid` parameters.')
        
        services.RefreshSteamGameDetails.execute({'steam_game': steam_game})
        