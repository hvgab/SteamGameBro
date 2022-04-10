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
        if random_game.has_detailed_info is False:
            services.refresh_steam_game_details(random_game.id)
        
        # Get system default group (yes, no)
        # system_game_groups = GameGroup.objects.filter(is_system_group=True).all()
        no_group = GameGroup.objects.get(is_system_group=True, name='NO')
        yes_group = GameGroup.objects.get(is_system_group=True, name='YES')
        
        return render(request, 'tinder.html', context={'game':random_game, 'no_group':no_group, 'yes_group':yes_group})
        
        # Get a random game
        # Let user choose YES or NO
        # POST
        # Redirect to same page
