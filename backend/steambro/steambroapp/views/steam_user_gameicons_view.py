from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from ..models import UserGameGroup
from steamlib import SteamUser as SteamUserAPI
from ..models import SteamUser
from ..models import SteamGame
from pprint import pprint, pformat
import logging

logger = logging.getLogger(__name__)

# Create your views here.
class SteamUserGameIconsView(ListView):
    model = SteamGame
    template_name = 'steambroapp/steamuser_gameicons.html'

    def get_queryset(self):
        # user = self.request.user
        user_id = self.kwargs['pk']
        steam_user = SteamUser.objects.get(id=user_id)
        games = steam_user.games.all()
        return games

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['pk']
        steam_user = SteamUser.objects.get(id=user_id)
        user_game_groups = UserGameGroup.objects.filter(user=steam_user).all()
        game_group_list = []
        for game in context['steamgame_list']:
            found_ugg = False
            for ugg in user_game_groups:
                if game.id == ugg.game.id:
                    found_ugg = True
                    game_group_list.append({'game':game, 'group':ugg.group})
            if found_ugg is False:
                game_group_list.append({'game':game, 'group':None})
            
        context['game_group_list'] = game_group_list

        return context


