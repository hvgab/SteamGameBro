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
from .. import services

log = logging.getLogger(__name__)

class TinderView(View):
    def get(self, request):

        user = self.request.user
        steam_user = SteamUser.objects.get(steamid=user.steamid)
        categorized_games = UserGameGroup.objects.filter(user=steam_user)
        categorized_games_count = UserGameGroup.objects.filter(user=steam_user).count()
        uncategorized_games = steam_user.games.exclude(id__in=categorized_games)
        uncategorized_games_count = steam_user.games.exclude(id__in=categorized_games).count()

        # game = uncategorized_games.first()
        # random game
        game_pks = uncategorized_games.values_list('pk', flat=True)
        random_pk = random.choice(game_pks)
        random_game = SteamGame.objects.get(pk=random_pk)

        # refresh game?
        if random_game.has_detailed_info is False:
            log.debug(f'Game {random_game} does not have detailed info. Running service')
            services.RefreshSteamGameDetails.execute({'steam_game':random_game})
            random_game.refresh_from_db()

        if random_game.type != 'game':
            redirect('steambro:tinder')

        # Get system default group (yes, no)
        # system_game_groups = GameGroup.objects.filter(is_system_group=True).all()
        no_group = GameGroup.objects.get(is_system_group=True, name='NO')
        yes_group = GameGroup.objects.get(is_system_group=True, name='YES')
        
        game_api_info = random_game.get_api_info()

        return render(request, 'tinder.html', context={
            'game':random_game, 
            'no_group':no_group, 
            'yes_group':yes_group, 
            'categorized_games_count':categorized_games_count, 
            'uncategorized_games_count':uncategorized_games_count,
            'game_api_info': game_api_info
            })
        
        # Get a random game
        # Let user choose YES or NO
        # POST
        # Redirect to same page
