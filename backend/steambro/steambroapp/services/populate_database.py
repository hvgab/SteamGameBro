import logging
from ..models import SteamUser
from ..models import SteamGame
from pprint import pprint

logger = logging.getLogger(__name__)

class Populator():
    def __init__(self):
        self.players_synced = []

    def run(self, steamid, sync_friends_level):
        logger.info(f'###\nPopulating {steamid!r}\nLevel {sync_friends_level}\n###')

        # update player
        player, created = SteamUser.objects.get_or_create(steamid=steamid)

        if player.steamid not in self.players_synced:
            
            # Refresh summary if player is just created
            player.refresh_summary()

            # get games
            player.refresh_steam_games()

            # get friends
            friends = player.refresh_friendships()
            
        self.players_synced.append(player.steamid)

        if sync_friends_level > 0 and friends is not None:
            for friend in friends.all():
                self.run(friend.steamid, sync_friends_level-1)


