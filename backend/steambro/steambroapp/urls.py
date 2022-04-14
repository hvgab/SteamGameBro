from django.urls import path
from django.contrib.auth.decorators import login_required

from .views.tinder import TinderView
from .api.views import SteamGameViewSet, SteamUserViewSet, UserGameGroupViewSet
from rest_framework import routers
from .views import IndexView, SteamUserListView, SteamUserDetailView, SteamUserGamesListView
from .views import SteamGameListView, SteamGameDetailView, SteamUserGameIconsView, SteamUserFriendsNetworkView, NetworkView, NetworkSigmaView
from .views import UserGameListView, UserFriendListView, couch_home
from django.urls import path, include

app_name = 'steambro'

router = routers.DefaultRouter()
router.register('api-steam-game', SteamGameViewSet)
router.register('api-steam-user', SteamUserViewSet)
router.register('api-user-game-group', UserGameGroupViewSet)

urlpatterns = [
    # API
    path('api/', include((router.urls, 'steambro-api'), namespace='steambro-api')),
    
    # APP
    path('', IndexView.as_view(), name='index'),

    # SteamUser
    path('steamuser/', SteamUserListView.as_view(), name='steamuser-list'),
    path('steamuser/<int:pk>', SteamUserDetailView.as_view(), name='steamuser-detail'),
    path('steamuser/<int:pk>/games', SteamUserGamesListView.as_view(), name='steamuser-games-list'),
    path('steamuser/<int:pk>/game-icons', SteamUserGameIconsView.as_view(), name='steamuser-gameicons'),
    path('steamuser/<int:pk>/friends-network', SteamUserFriendsNetworkView.as_view(), name='steamuser-friends-network'),
    
    path('network/', NetworkView.as_view(), name='network'),
    path('network-sigma/', NetworkSigmaView.as_view(), name='network'),

    path('steamgames/', SteamGameListView.as_view(), name='steamgame-list'),
    path('steamgames/<int:pk>', SteamGameDetailView.as_view(), name='steamgame-detail'),


    path('user/gamelist', UserGameListView.as_view(), name='usergamelist'),
    path(
        'user/friendlist', UserFriendListView.as_view(),
        name='userfriendlist'),
    path('couch', couch_home, name='couch_home'),
    
    path('tinder/', TinderView.as_view(), name='tinder'),


]
