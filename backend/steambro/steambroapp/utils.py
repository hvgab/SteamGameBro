from steambroapp.models import SteamUser, SteamGame
from time import sleep
import datetime as dt
from django.utils import timezone
import logging
from celery import shared_task

log = logging.getLogger(__name__)

def sync_player_last_update_check(player: SteamUser):
    compare_time = timezone.now() + dt.timedelta(days=-1)
    if (player.updated_at is None) or (player.updated_at < compare_time):
        return True
    return False

@shared_task()
def sync_player(self, steamid, sync_friend_levels=3):
    """Update playerdata from api to database"""
        
    log.info(f'Syncing player {steamid!r}')
    
    player, created = SteamUser.objects.get_or_create(steamid=steamid)
    
    if not sync_player_last_update_check():
        return
    
    # get games
    player.get_steam_games()
    
    # get friends
    if sync_friend_levels > 0:
        friends = player.get_steam_friends()
        for friend in friends:
            f = SteamUser.objects.get_or_create(steamid=steamid)
            if sync_player_last_update_check():
                # do celery player sync
                sync_player(f.steamid, sync_friend_levels=sync_friend_levels-1)