from django.urls import path
from django.contrib.auth.decorators import login_required
from steambroapp.api.views import SteamGameViewSet, SteamUserViewSet
from rest_framework import routers
from .views import IndexView, SteamUserListView, SteamUserDetailView, SteamUserGamesListView
from .views import UserGameListView, UserFriendListView, couch_home
from django.urls import path, include

app_name = 'steambro'

router = routers.DefaultRouter()
router.register('steam-game', SteamGameViewSet)
router.register('steam-user', SteamUserViewSet)

urlpatterns = [
    # API
    path('api/', include(router.urls)),
    
    # APP
    path('', IndexView.as_view(), name='index'),

    # SteamUser
    path('steamuser/', SteamUserListView.as_view(), name='steam-user-list-view'),
    path('steamuser/<pk>', SteamUserDetailView.as_view(), name='steam-user-detail-view'),
    path('steamuser/<pk>/games', SteamUserGamesListView.as_view(), name='steam-user-games-list-view'),

    


    path('user/gamelist', UserGameListView.as_view(), name='usergamelist'),
    path(
        'user/friendlist', UserFriendListView.as_view(),
        name='userfriendlist'),
    path('couch', couch_home, name='couch_home'),
]
