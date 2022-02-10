from django.core.management.base import BaseCommand, CommandError
from steambroapp.models import SteamUser, SteamGame
from time import sleep
import datetime as dt
from django.utils import timezone
import logging
from steambroapp.utils import sync_player
from ... import service

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Recursivly add Gabbeh, friends and everyones games.'

    def add_arguments(self, parser):
        parser.add_argument('--levels', type=int)
        parser.add_argument('--steamid', type=int)

    def handle(self, *args, **kwargs):

        logger.debug(kwargs)
        
        steamid = 76561197983132487
        if 'steamid' in kwargs and kwargs['steamid'] is not None:
            steamid = kwargs['steamid']

        levels = 2
        if 'levels' in kwargs and kwargs['levels'] is not None:
            levels = kwargs['levels']
                
        populator = service.Populator()
        populator.run(steamid, levels)
