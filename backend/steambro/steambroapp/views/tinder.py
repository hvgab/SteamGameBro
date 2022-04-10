from django.shortcuts import render, redirect
from django.views import View
from ..models import GameGroup
from steamlib import SteamUser as SteamUserAPI
from ..models import SteamUser
from ..models import SteamGame
from ..models import UserGameGroup
from pprint import pprint, pformat
import logging
import random

log = logging.getLogger(__name__)

class TinderView(View):
    def get(self, request):

        user = self.request.user
        steam_user = SteamUser.objects.get(steamid=user.steamid)
        categorized_games = UserGameGroup.objects.filter(user=steam_user)
        uncategorized_games = steam_user.games.exclude(id__in=categorized_games)

        # game = uncategorized_games.first()
        # random game
        game_pks = uncategorized_games.values_list('pk', flat=True)
        random_pk = random.choice(game_pks)
        random_game = SteamGame.objects.get(pk=random_pk)

        # refresh game?
        
        # Get system default group (yes, no)
        # system_game_groups = GameGroup.objects.filter(is_system_group=True).all()
        no_group = GameGroup.objects.get(is_system_group=True, name='NO')
        yes_group = GameGroup.objects.get(is_system_group=True, name='YES')
        
        return render(request, 'tinder.html', context={'game':random_game, 'no_group':no_group, 'yes_group':yes_group})
        
        # Get a random game
        # Let user choose YES or NO
        # POST
        # Redirect to same page


        
    


class UserFriendListView(View):
    def get(self, request, steamid=None):
    
        if not (request.user.is_authenticated or steamid):
            return redirect('steambro:index')

        if not steamid:
            steamid = request.user.steamid
        
        # Get steam games from API
        steamUserAPI = SteamUserAPI(request.user.steamid)
        players = steamUserAPI.getFriendList()
        # players_API = players['friendslist']['friends']
        players_API = players

        # friend_list_API = [fgame['appid'] for game in games_API]
        # print(f'appID API: {appID_list_API}')

        # Get all games in DB
        all_players_DB = SteamUser.objects.all()
        player_list_DB = [player.steamid for player in all_players_DB]
        log.debug(f'\n\nplayer_list_DB: \n\n{player_list_DB}')
        print(f'steamID_list_DB: {player_list_DB}')

        # Create cache or games not in DB.
        # Slows down original request, but speeds up later.
        for player in players_API:
            player_steamid = None
            try:
                player_steamid = int(player['steamid'])
            except Exception as e:
                log.error(f'steamid not int. ({player["steamid"]})')
                continue
            
            if player_steamid is None:
                continue
            
            if player_steamid in player_list_DB:
                log.debug(f'{player_steamid} in db (all)')
                continue

            # TODO: Why do I have to check again here?
            if SteamUser.objects.filter(steamid = player_steamid).count() > 0:
                log.debug(f'{player_steamid} in db (single)')
                continue

            # If user does not exist, get and save.
            log.info(f'player {player_steamid} not in db')
            # get player data
            playerAPI = SteamUserAPI(player_steamid)
            playerAPI.getPlayerSummaries()
            player_instance = SteamUser(
                    steamid = playerAPI.steamid,
                    personaname = playerAPI.personaname,
                    profileurl = playerAPI.profileurl,
                    avatar = playerAPI.avatar,
                    avatarmedium = playerAPI.avatarmedium,
                    avatarfull = playerAPI.avatarfull
            )
            player_instance.save()
            log.info(f'player {playerAPI.personaname} ({playerAPI.steamid}) saved to db')
        else:
            log.debug(f'player {player_steamid} already in db')
                

        # Get games from DB
        player_list_API = [player['steamid'] for player in players_API]
        players_DB = SteamUser.objects.filter(steamid__in=player_list_API).all()

        return render(
            request, 'userfriendlist.html', context={'playerlist':players_DB, 'friendlist':players_DB})
