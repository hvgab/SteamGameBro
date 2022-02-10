from .steam_user_views import SteamUserListView, SteamUserDetailView, SteamUserGamesListView
from django.views.generic import TemplateView

from .fuckviews import couch_home, UserFriendListView, UserGameListView

class IndexView(TemplateView):
    template_name = 'index.html'