import requests
import os
from pprint import pprint
import logging
from pprint import pprint
from django.conf import settings

log = logging.getLogger(__name__)

class SteamUser(object):
    """classd doc"""

    def __init__(self, steamid):
        self.steamid = steamid

        self.communityvisibilitystate = None
        self.personaname = None
        self.profileurl = None
        self.avatar = None
        self.avatarmedium = None
        self.avatarfull = None
        self.personastate = None

        log.debug(f'init SteamUser {self.steamid}')
        if not self.steamid.startswith('765'):
            self.resolveVanityUrl()

    def __repr__(self):
        return f'<SteamUser({self.steamid}, {self.personaname})>'

    def to_dict(self):
        return dict(
            steamid=self.steamid,
            communityvisibilitystate=self.communityvisibilitystate,
            personaname=self.personaname,
            profileurl=self.personaname,
            avatar=self.avatar,
            avatarmedium=self.avatarmedium,
            avatarfull=self.avatarfull,
            personastate=self.personastate)

    def getPlayerSummaries(self):
        log.debug('start getPlayerSummaries')
        ISteamUser_GetPlayerSummaries_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'

        payload = {'key': settings.STEAM_API_KEY, 'steamids': self.steamid}

        r = requests.get(ISteamUser_GetPlayerSummaries_url, params=payload)
        try:
            rj = r.json()
            pprint(rj)
            log.debug(rj)
            self.steamid = rj['response']['players'][0]['steamid']
            self.personaname = rj['response']['players'][0]['personaname']
            self.profileurl = rj['response']['players'][0]['profileurl']
            self.avatar = rj['response']['players'][0]['avatar']
            self.avatarmedium = rj['response']['players'][0]['avatarmedium']
            self.avatarfull = rj['response']['players'][0]['avatarfull']
            self.personastate = rj['response']['players'][0]['personastate']
        except Exception as e:
            raise ValueError('request error. \n{r.test}')        

    def resolveVanityUrl(self):
        log.debug(f'Resolve Vanity URL for {self.steamid!r}')
        resolveVanityUrl_url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
        payload = {
            'key': os.getenv('STEAM_API_KEY'),
            'vanityurl': self.steamid
        }

        r = requests.get(resolveVanityUrl_url, params=payload)
        # If match; change steamid
        try:
            r_json = r.json()
            if ('response' in r_json) and (r_json['response']['success'] == 1):
                log.info(f'Resolved vanity ID for {self.steamid!r} to {r_json["response"]["steamid"]!r}')
                self.steamid = r_json['response']['steamid']
        except Exception as e:
            log.debug(f'No JSON in request response. Payload: {payload}')

    def getFriends(self):
        friends = {}
        ISteamUser_GetFriendList_url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
        payload = {
            # 'key': os.getenv('STEAM_API_KEY'),
            'key': settings.STEAM_API_KEY,
            'steamid': self.steamid
            #'relationship' : 'friend'
        }
        r = requests.get(ISteamUser_GetFriendList_url, params=payload)
        r.raise_for_status()

        result = r.json()

        friendlist = []

        for friend in result['friendslist']['friends'][:5]:
            log.debug(friend)
            friendObject = SteamUser(friend['steamid'])
            friendObject.getPlayerSummaries()
            log.debug(friendObject.personaname)
            friendlist.append(friendObject.to_dict())
        return friendlist

    def getFriendList(self):
        friends = {}
        ISteamUser_GetFriendList_url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
        payload = {
            'key': settings.STEAM_API_KEY,
            'steamid': self.steamid
            #'relationship' : 'friend'
        }
        r = requests.get(ISteamUser_GetFriendList_url, params=payload)
        log.debug(payload['key'])
        r.raise_for_status()

        return r.json()['friendslist']['friends']

    def getOwnedGames(self):
        ISteamUser_GetOwnedGames_url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
        payload = {
            'key': settings.STEAM_API_KEY,
            'steamid': self.steamid,
            'include_appinfo': 1,
            'include_played_free_games': 1,
            'format': 'json'
        }
        r = requests.get(ISteamUser_GetOwnedGames_url, params=payload)
        r.raise_for_status()
        try:
            result = r.json()
        except Exception as e:
            log.debug(e)
            log.debug(f'payload: {payload}')
            log.debug(r.text)
            result = None
        return result

    def getOwnedGameImgURL(self, appid, hash):
        return f'http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg'


if __name__ == "__main__":

    #u = steamUser('76561197983132487')
    u = steamUser('gabbeh')
    # log.debug (u)
    friends = u.getFriendList()
    games = u.getOwnedGames()

    log.debug('u.personaname: {}'.format(u.personaname))
    log.debug('u.id: {}'.format(u.steamid))
    log.debug('u.steamid: {}'.format(u.steamid))
    #log.debug ( friends )
    log.debug(games)
    for k, v in u.getFriendList():
        log.debug('\n{}\n{}\n'.format(k, v))
