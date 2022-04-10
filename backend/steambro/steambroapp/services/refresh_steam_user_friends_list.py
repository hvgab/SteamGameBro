from asyncio.log import logger
from django.conf import settings
import logging
import requests
from pprint import pprint
import datetime as dt
logger = logging.getLogger(__name__)

def refresh_steam_user_friends_list(steam_user:'SteamUser'):
    from ..models import SteamUser
    ISteamUser_GetFriendList_url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
    payload = {
        'key': settings.STEAM_API_KEY,
        'steamid': steam_user.steamid
        #'relationship' : 'friend'
    }
    r = requests.get(ISteamUser_GetFriendList_url, params=payload)
    r.raise_for_status()

    rj = r.json()
    logger.debug('Are all friends "friend"? START')
    for f in rj['friendslist']['friends']:
        if f['relationship'].lower() != 'friend':
            logger.warn(pprint(f))
    logger.debug('Are all friends "friend"? END')
    

    for friendship_friend in rj['friendslist']['friends']:
        logger.debug(friendship_friend)
        
        friend, created = SteamUser.objects.get_or_create(steamid=friendship_friend['steamid'])
        if created is True:
            friend.save()

        friendship_dt = dt.datetime.utcfromtimestamp(friendship_friend['friend_since'])
        steam_user.add_friendship(friend, friendship_dt, friendship_friend['relationship'])
    # return friendlist