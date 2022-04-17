from .steam_user_views import SteamUserListView, SteamUserDetailView, SteamUserGamesListView
from .steam_game_views import *
from .steam_user_gameicons_view import *
from .steam_user_friends_network import *
from .network import *
from .network_sigma import *
from .steam_group_network import *

from django.views.generic import TemplateView

from .fuckviews import couch_home, UserFriendListView, UserGameListView

class IndexView(TemplateView):
    template_name = 'index.html'