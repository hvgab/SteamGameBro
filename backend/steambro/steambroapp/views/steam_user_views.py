from django.views.generic import ListView, DetailView
from ..models import SteamUser, SteamGame
import logging
from django.db.models import QuerySet
from pprint import pprint

logger = logging.getLogger(__name__)

class SteamUserListView(ListView):
    model = SteamUser

class SteamUserDetailView(DetailView):
    model = SteamUser

class SteamUserGamesListView(ListView):
    """All games of user"""
    model = SteamGame
    # template_name = 'steamuser_games_list.html'

    def get_queryset(self) -> QuerySet[SteamGame]:
        logger.debug('get queryset user game list')
        user = SteamUser.objects.get(steamid = self.request.user.steamid)
        logger.debug(pprint(user))
        games = user.games
        logger.debug(pprint(games))
        return games

