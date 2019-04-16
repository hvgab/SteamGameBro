from django.shortcuts import render, redirect
from django.views import View
from steamlib import SteamUser as SteamUserAPI
from .models import SteamUser
from .models import SteamGame


def couch_home(request):
    print(request.user.steamid)
    host = SteamUser.manager.get_or_api(steamid=request.user.steamid)
    # friends = SteamUser.objects.get(steamid=request.user.steamid)

    steam_user_ids = request.GET.get('steam_user_ids', None)

    # if ',' in steam_user_ids:
    if steam_user_ids:
        print(steam_user_ids)
        steam_user_ids = steam_user_ids.split(',')
        print(steam_user_ids)
        users = list(
            SteamUser.objects.filter(steamid__in=steam_user_ids).all())
    else:
        users = []
    print(users)
    return render(request, 'couch_home.html', context={'users': users})


# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class UserGameListView(View):
    def get(self, request, steamid=None):

        if not (request.user.is_authenticated or steamid):
            return redirect('steam:index')

        if not steamid:
            steamid = request.user.steamid
        # if request.GET.get('update_game_list') == 1:
        # pass
        # Get steam games from API
        steamUserAPI = SteamUserAPI(request.user.steamid)
        gamelistresponse = steamUserAPI.getOwnedGames()
        gamelistAPI = gamelistresponse['response']['games']

        appidlistAPI = [game['appid'] for game in gamelistAPI]

        # Get from DB
        # Getting from DB to serve imgs from own server.
        gamelistDB = list(SteamGame.objects.filter(id__in=appidlistAPI).all())
        print(gamelistDB)
        appidlistDB = [game.appid for game in gamelistDB]
        print(appidlistDB)
        # Create cache or games not in DB.
        # Slows down original request, but speeds up later.
        refresh_gamelistDB = False
        for game in gamelistAPI:
            if game['appid'] not in appidlistDB:
                refresh_gamelistDB = True
                print(f'game {game["name"]} not in gamelistDB')
                # del some keys to use kwargs
                del_keys = [
                    'playtime_forever', 'playtime_2weeks',
                    'has_community_visible_stats'
                ]
                for key in del_keys:
                    if key in game:
                        del game[key]
                # del game['playtime_forever']
                # del game['has_community_visible_stats']
                # del game['playtime_2weeks']
                game_instance = SteamGame(**game)
                print(f'game_instance: {game_instance}')
                game_instance.save()
                print('game_instance saved.')

        if refresh_gamelistDB:
            gamelistDB = list(
                SteamGame.objects.filter(id__in=appidlistAPI).all())

        return render(
            request, 'usergamelist.html', context=dict(gamelist=gamelistDB))


class UserFriendListView(View):
    def get(self, request, steamid=None):
        if not request.user.is_authenticated:
            return redirect('steam:index')

        # if request.GET.get('update_game_list') == 1:
        # pass
        # Get steam games from API
        # steamUser = SteamUserAPI.manager.get(request.user.steamid)
        # friendlist = steamUser.getFriends()

        return render(
            request,
            'userfriendlist.html',
            context=dict(friendlist=friendlist))
