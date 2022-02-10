from asyncio.log import logger
from django.conf import settings
from ..models import SteamUser
import logging
import requests
from pprint import pprint

logger = logging.getLogger(__name__)

def refresh_steam_user_summary(steam_user:SteamUser):

    logger.debug('start getPlayerSummaries')
    ISteamUser_GetPlayerSummaries_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    payload = {'key': settings.STEAM_API_KEY, 'steamids': steam_user.steamid}
    r = requests.get(ISteamUser_GetPlayerSummaries_url, params=payload)

    try:
        rj = r.json()
        pprint(rj)
        logger.debug(rj)
    except Exception as e:
        raise ValueError('request error. \n{r.test}') 
    
    steam_user.steamid = rj['response']['players'][0]['steamid']
    steam_user.personaname = rj['response']['players'][0]['personaname']
    steam_user.profileurl = rj['response']['players'][0]['profileurl']
    steam_user.avatar = rj['response']['players'][0]['avatar']
    steam_user.avatarmedium = rj['response']['players'][0]['avatarmedium']
    steam_user.avatarfull = rj['response']['players'][0]['avatarfull']
    steam_user.personastate = rj['response']['players'][0]['personastate']
    steam_user.save()