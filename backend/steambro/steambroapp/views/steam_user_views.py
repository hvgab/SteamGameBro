from django.views.generic import ListView, DetailView
from ..models import SteamUser, SteamGame
import logging
from django.db.models import QuerySet
from pprint import pprint

logger = logging.getLogger(__name__)

class SteamUserListView(ListView):
    model = SteamUser
    paginate_by = 50

class SteamUserDetailView(DetailView):
    model = SteamUser
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['steamuser'].refresh_summary()
        return context

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

