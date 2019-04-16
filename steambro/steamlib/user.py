import requests
import os

print('osgetenv')
print(os.getenv('STEAM_API_KEY'))


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

        print(f'init SteamUser {self.steamid}')
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
        print('start getPlayerSummaries')
        ISteamUser_GetPlayerSummaries_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'

        payload = {'key': os.getenv('STEAM_API_KEY'), 'steamids': self.steamid}

        r = requests.get(ISteamUser_GetPlayerSummaries_url, params=payload)
        rj = r.json()

        print(rj)
        # print('rj: ', rj)
        self.steamid = rj['response']['players'][0]['steamid']
        # self.communityvisibilitystate = rj['response'][
        # 'communityvisibilitystate'][0]
        self.personaname = rj['response']['players'][0]['personaname']
        self.profileurl = rj['response']['players'][0]['profileurl']
        self.avatar = rj['response']['players'][0]['avatar']
        self.avatarmedium = rj['response']['players'][0]['avatarmedium']
        self.avatarfull = rj['response']['players'][0]['avatarfull']
        self.personastate = rj['response']['players'][0]['personastate']
        # self. = rj['response']['players'][0]
        # self.friendList = getFriendList()

    def resolveVanityUrl(self):
        resolveVanityUrl_url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
        payload = {
            'key': os.getenv('STEAM_API_KEY'),
            'vanityurl': self.steamid
        }

        r = requests.get(resolveVanityUrl_url, params=payload)
        # If match; change steamid
        try:
            r_json = r.json()
            if not ('response' in r_json) and (
                    r_json['response']['message'] == 'No match'):
                self.steamid = vanity
        except Exception as e:
            print(f'No JSON in request response. Payload: {payload}')

    def getFriends(self):
        friends = {}
        ISteamUser_GetFriendList_url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
        payload = {
            'key': os.getenv('STEAM_API_KEY'),
            'steamid': self.steamid
            #'relationship' : 'friend'
        }
        r = requests.get(ISteamUser_GetFriendList_url, params=payload)
        r.raise_for_status()

        result = r.json()

        friendlist = []

        for friend in result['friendslist']['friends'][:5]:
            print(friend)
            friendObject = SteamUser(friend['steamid'])
            friendObject.getPlayerSummaries()
            print(friendObject.personaname)
            friendlist.append(friendObject.to_dict())
        return friendlist

    def getFriendList(self):
        friends = {}
        ISteamUser_GetFriendList_url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
        payload = {
            'key': os.getenv('STEAM_API_KEY'),
            'steamid': self.steamid
            #'relationship' : 'friend'
        }
        r = requests.get(ISteamUser_GetFriendList_url, params=payload)
        r.raise_for_status()

        return r.json()['friendslist']['friends']

    def getOwnedGames(self):
        ISteamUser_GetOwnedGames_url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
        payload = {
            'key': os.getenv('STEAM_API_KEY'),
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
            print(e)
            print(f'payload: {payload}')
            print(r.text)
            result = None
        return result

    def getOwnedGameImgURL(self, appid, hash):
        return f'http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg'


if __name__ == "__main__":

    #u = steamUser('76561197983132487')
    u = steamUser('gabbeh')
    # print (u)
    friends = u.getFriendList()
    games = u.getOwnedGames()

    print('u.personaname: {}'.format(u.personaname))
    print('u.id: {}'.format(u.steamid))
    print('u.steamid: {}'.format(u.steamid))
    #print ( friends )
    print(games)
    for k, v in u.getFriendList():
        print('\n{}\n{}\n'.format(k, v))
