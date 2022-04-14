from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from steamlib import SteamUser as SteamUserAPI
from ..models import SteamUser
from ..models import SteamGame
from pprint import pprint, pformat
import logging

log = logging.getLogger(__name__)

# Create your views here.
class SteamUserGameIconsView(ListView):
    model = SteamGame
    template_name = 'steambroapp/steamuser_gameicons.html'

    def get_queryset(self):
        user = self.request.user
        steam_user = SteamUser.objects.get(steamid=user.steamid)
        games = steam_user.games.all()
        return games



