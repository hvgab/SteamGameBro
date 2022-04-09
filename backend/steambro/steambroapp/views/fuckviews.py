from django.shortcuts import render, redirect
from django.views import View
from steamlib import SteamUser as SteamUserAPI
from ..models import SteamUser
from ..models import SteamGame
from pprint import pprint, pformat
import logging

log = logging.getLogger(__name__)

def couch_home(request):
    log.debug(f'req user: {request.user.steamid}')
    host = SteamUser.objects.get(steamid=request.user.steamid)
    # friends = SteamUser.objects.get(steamid=request.user.steamid)

    steam_user_ids = request.GET.get('steam_user_ids', None)

    # if ',' in steam_user_ids:
    id64_steam_user_ids = []
    if steam_user_ids:
        steam_user_ids = steam_user_ids.split(',')
                
        for id in steam_user_ids:
            if not id.startswith('765'):
                log.debug(f'ID {id!r} does not start with 765')
                id = SteamUserAPI(id).steamid
            id64_steam_user_ids.append(id)

        log.debug(f'id64 user ids: {id64_steam_user_ids}')


        
        users = SteamUser.objects.filter(steamid__in=id64_steam_user_ids).all()
    else:
        users = []
    log.debug(f'users: {users}')
    return render(request, 'couch_home.html', context={'users': users})


# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class UserGameListView(View):
    def get(self, request, steamid=None):

        if not (request.user.is_authenticated or steamid):
            return redirect('steambro:index')

        if not steamid:
            steamid = request.user.steamid
        
        # Get steam games from API
        steamUserAPI = SteamUserAPI(request.user.steamid)
        owned_games = steamUserAPI.getOwnedGames()
        games_API = owned_games['response']['games']

        appID_list_API = [game['appid'] for game in games_API]
        log.debug(appID_list_API)
        print(f'appID API: {appID_list_API}')

        # Get all games in DB
        all_games_DB = SteamGame.objects.all()
        appID_list_DB = [game.appid for game in all_games_DB]
        print(f'appID_list_DB: {appID_list_DB}')

        user = SteamUser.get(steamid=steamid)
        user_owns = user.games

        # Create cache or games not in DB.
        # Slows down original request, but speeds up later.
        for game in games_API:
            if game['appid'] not in appID_list_DB:
                log.info(f'game {game["name"]} not in db')
                log.debug(pformat(game))
                img_logo_url = None
                try:
                    img_logo_url = game['img_logo_url']
                except:
                    pass
                game_instance = SteamGame(appid=game['appid'], icon_url=game['img_icon_url'], logo_url=img_logo_url, name=game['name'])
                game_instance.save()
                log.info(f'game {game["name"]} saved to db')
            else:
                log.debug(f'game {game["name"]} already in db')

            # add as owned
            if game['appid'] not in user.games:
                game_ = SteamGame.get(appid=game['appid'])
                user.games.add(game_)
                

        # Get games from DB
        log.debug(appID_list_API)
        games_DB = SteamGame.objects.filter(id__in=appID_list_API)
        log.debug(games_DB)
        return render(
            request, 'usergamelist.html', context=dict(games=list(games_DB.all()), games_query=games_DB))


class UserFriendListView(View):
    def get(self, request, steamid=None):
    
        if not (request.user.is_authenticated or steamid):
            return redirect('steambro:index')

        if not steamid:
            steamid = request.user.steamid
        
        # Get steam games from API
        steamUserAPI = SteamUserAPI(request.user.steamid)
        players = steamUserAPI.getFriendList()
        # players_API = players['friendslist']['friends']
        players_API = players

        # friend_list_API = [fgame['appid'] for game in games_API]
        # print(f'appID API: {appID_list_API}')

        # Get all games in DB
        all_players_DB = SteamUser.objects.all()
        player_list_DB = [player.steamid for player in all_players_DB]
        log.debug(f'\n\nplayer_list_DB: \n\n{player_list_DB}')
        print(f'steamID_list_DB: {player_list_DB}')

        # Create cache or games not in DB.
        # Slows down original request, but speeds up later.
        for player in players_API:
            player_steamid = None
            try:
                player_steamid = int(player['steamid'])
            except Exception as e:
                log.error(f'steamid not int. ({player["steamid"]})')
                continue
            
            if player_steamid is None:
                continue
            
            if player_steamid in player_list_DB:
                log.debug(f'{player_steamid} in db (all)')
                continue

            # TODO: Why do I have to check again here?
            if SteamUser.objects.filter(steamid = player_steamid).count() > 0:
                log.debug(f'{player_steamid} in db (single)')
                continue

            # If user does not exist, get and save.
            log.info(f'player {player_steamid} not in db')
            # get player data
            playerAPI = SteamUserAPI(player_steamid)
            playerAPI.getPlayerSummaries()
            player_instance = SteamUser(
                    steamid = playerAPI.steamid,
                    personaname = playerAPI.personaname,
                    profileurl = playerAPI.profileurl,
                    avatar = playerAPI.avatar,
                    avatarmedium = playerAPI.avatarmedium,
                    avatarfull = playerAPI.avatarfull
            )
            player_instance.save()
            log.info(f'player {playerAPI.personaname} ({playerAPI.steamid}) saved to db')
        else:
            log.debug(f'player {player_steamid} already in db')
                

        # Get games from DB
        player_list_API = [player['steamid'] for player in players_API]
        players_DB = SteamUser.objects.filter(steamid__in=player_list_API).all()

        return render(
            request, 'userfriendlist.html', context={'playerlist':players_DB, 'friendlist':players_DB})
