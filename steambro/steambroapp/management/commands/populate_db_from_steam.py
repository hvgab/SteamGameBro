from django.core.management.base import BaseCommand, CommandError
from steambroapp.models import SteamUser, SteamGame
from time import sleep
import datetime as dt
from django.utils import timezone
import logging

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Recursivly add Gabbeh, friends and everyones games.'

    def __init__(self):
        super().__init__()
        self.steamids_synced = []

    def handle(self, *args, **kwargs):
        steamid = 76561197983132487
        # if options['steamid'] is not None:
            # steamid = options['steamid']
        
        self.sync_player(steamid)

    def print_status(self):
        print('\n\n\n\n\n')
        log.info(f'Synced: {len(self.steamids_synced)}')
        log.info('Current DB Inventory:\n')
        player_count = SteamUser.objects.count()
        log.info(f'Player Count: {player_count}')
        game_count = SteamGame.objects.count()
        log.info(f'Game Count: {game_count}')
        print('\n\n')
        sleep(2)

    def sync_player(self, steamid):
        log.info(f'Syncing player {steamid!r}')
        self.steamids_synced.append(steamid)
        # update player
        player, created = SteamUser.objects.get_or_create(steamid=steamid)
        compare_time = timezone.now() + dt.timedelta(days=-1)

        # log.debug(f'player last update: {player.updated_at}')
        # log.debug(f'compare time: {compare_time}')
        
        # log.debug(f'{player.updated_at} < {compare_time}?')
        # log.debug(player.updated_at < compare_time)
        
        if (player.updated_at is None) or (player.updated_at < compare_time):
            player.update_steam_player_summary()

        log.debug(f'player: {player.steamid}')
        # get games
        player.get_steam_games()
        # get friends
        friends = player.get_steam_friends()
        
        if friends is None:
            return

        for friend in friends:
            if friend.steamid in self.steamids_synced:
                continue
            self.print_status()
            self.sync_player(friend.steamid)