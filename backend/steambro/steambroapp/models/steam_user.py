import pprint
import django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_comma_separated_integer_list
import logging
from django.conf import settings
import requests
import json
from django.utils import timezone
import datetime as dt
from django.db import transaction
from progress.bar import Bar

logger = logging.getLogger(__name__)


class SteamUser(models.Model):
    ## Public Data
    
    # steamid - 64bit SteamID of the user
    steamid = models.BigIntegerField(unique=True, help_text="64bit SteamID of the user")
    steamid_text = models.CharField(max_length=255, blank=True, null=True)
    
    # personaname
    # The player's persona name (display name)
    personaname = models.CharField(max_length=255, blank=True, null=True, help_text="The player's persona name (display name)")
    
    # profileurl
    # The full URL of the player's Steam Community profile.
    profileurl = models.CharField(max_length=500, blank=True, null=True)
    
    # avatarhash
    avatarhash = models.CharField(max_length=500, blank=True, null=True)

    # avatar
    # The full URL of the player's 32x32px avatar. 
    # If the user hasn't configured an avatar, this will be the default ? avatar.
    avatar = models.CharField(max_length=500, blank=True, null=True)
    
    # avatarmedium
    # The full URL of the player's 64x64px avatar. 
    # If the user hasn't configured an avatar, this will be the default ? avatar.
    avatarmedium = models.CharField(max_length=500, blank=True, null=True)
    
    # avatarfull
    # The full URL of the player's 184x184px avatar. 
    # If the user hasn't configured an avatar, this will be the default ? avatar.
    avatarfull = models.CharField(max_length=500, blank=True, null=True)
    
    # personastate 
    # The user's current status. 
    #   0 - Offline, 
    #   1 - Online, 
    #   2 - Busy, 
    #   3 - Away, 
    #   4 - Snooze, 
    #   5 - looking to trade, 
    #   6 - looking to play. 
    # If the player's profile is private, this will always be "0", 
    # except if the user has set their status to looking to trade or looking to play, 
    # because a bug makes those status appear even if the profile is private.
    personastate = models.IntegerField(_("personastate"), default=0)
    
    # communityvisibilitystate
    # This represents whether the profile is visible or not, 
    # and if it is visible, why you are allowed to see it. 
    # Note that because this WebAPI does not use authentication, 
    # there are only two possible values returned: 
    #   1 - the profile is not visible to you (Private, Friends Only, etc), 
    #   3 - the profile is "Public", and the data is visible. 
    #   Mike Blaszczak's post on Steam forums says, 
    #       "The community visibility state this API returns is different than the privacy state. 
    #       It's the effective visibility state from the account making the request 
    #       to the account being viewed given the requesting account's relationship to the viewed account."
    communityvisibilitystate = models.IntegerField(_("communityvisibilitystate"), default=1)

    # profilestate
    # If set, indicates the user has a community profile configured (will be set to '1')
    profilestate = models.IntegerField(_("profilestate"), default=0)
    
    # lastlogoff
    # The last time the user was online, in unix time. DJANGOAPP CONVERTS TO DATETIME BEFORE SAVE
    # Only available when you are friends with the requested user (since Feb, 4).
    lastlogoff = models.DateTimeField(_("lastlogoff"), auto_now=False, auto_now_add=False, null=True, blank=True)
    
    # commentpermission
    # If set, indicates the profile allows public comments.
    commentpermission = models.IntegerField(_("commentpermission"), default=0)
    
    
    ## Private Data
    
    # realname
    # The player's "Real Name", if they have set it.
    realname = models.CharField(_("realname"), max_length=500, null=True, blank=True)
    
    # primaryclanid
    # The player's primary group, as configured in their Steam Community profile.
    primaryclanid = models.BigIntegerField(_("primaryclanid"), null=True, blank=True)
    
    # timecreated
    # The time the player's account was created.
    timecreated = models.DateTimeField(_("timecreated"), auto_now=False, auto_now_add=False, null=True, blank=True)
    
    # gameid
    # If the user is currently in-game, this value will be returned and set to the gameid of that game.
    
    # gameserverip
    # The ip and port of the game server the user is currently playing on, if they are playing on-line in a game using Steam matchmaking. Otherwise will be set to "0.0.0.0:0".
    
    # gameextrainfo
    # If the user is currently in-game, this will be the name of the game they are playing. This may be the name of a non-Steam game shortcut.
    
    # cityid
    # This value will be removed in a future update (see loccityid)
    
    loccountrycode = models.CharField(_("country coude"), max_length=5, blank=True, null=True, help_text="If set on the user's Steam Community profile, The user's country of residence, 2-character ISO country code")
    
    locstatecode = models.CharField(_("state"), max_length=50, blank=True, null=True, help_text="If set on the user's Steam Community profile, The user's state of residence")
    
    # loccityid
    # An internal code indicating the user's city of residence. A future update will provide this data in a more useful way.
    # steam_location gem/package makes player location data readable for output.

    # personastateflags

    # lobbysteamid

    # gameserversteamid

    friendships_are_public = models.BooleanField(default=True)
    friendships_updated = models.DateTimeField(blank=True, null=True)


    owned_games_list = models.CharField(
        max_length=1000000,
        blank=True,
        validators=[validate_comma_separated_integer_list])
    
    games = models.ManyToManyField("steambroapp.SteamGame", verbose_name=_("games"), blank=True, null=True)
    friendships = models.ManyToManyField('self', verbose_name=_("friends"), through='Friendship', symmetrical=False, related_name='related_to')

    # SteamBro
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(_("created at"), auto_now=False, auto_now_add=True)
    objects = models.Manager()  # Default manager
    # manager = SteamUserManager()  # Custom manager

    def refresh_summary(self):
        """Refresh Steam User Summary from API to Database"""

        logger.debug(f'<SteamUser({self.steamid!r}, {self.personaname!r})>.refresh_summary()')

        url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'  # ISteamUser_GetPlayerSummaries
        payload = {'key': settings.STEAM_API_KEY, 'steamids': self.steamid}
        r = requests.get(url, params=payload)
        
        try:
            rj = r.json()
        except json.decoder.JSONDecodeError as e:
            logger.error(f'Json Decode Error on update steam player summary for {self.steamid}')
            return


        # Get Data
        if len(rj['response']['players']) <= 0:
            return

        player_api_dict = rj['response']['players'][0]
        # Get Public Data
        fields_as_int = ['personastate', 'communityvisibilitystate', 'profilestate', 'commentpermission', 'primaryclanid',]
        fields_unix_to_datetime = ['lastlogoff', 'timecreated',]
        fields_ignore = ['gameid', 'gameserverip', 'gameextrainfo', 'loccityid', 'personastateflags', 'lobbysteamid', 'gameserversteamid']

        for key in player_api_dict.keys():
            if (key in self.__dict__.keys()) and (key in player_api_dict.keys()):
                if key in fields_as_int:
                    setattr(self, key, int(player_api_dict[key]))
                elif key in fields_unix_to_datetime:
                    setattr(self, key, timezone.make_aware(dt.datetime.fromtimestamp(player_api_dict[key])))
                else:
                    setattr(self, key, player_api_dict[key])
            else:
                if key.lower() not in fields_ignore:
                    logger.warning(f'Key {key.upper()} not in class attributes')
                    logger.debug('player_api_dict')
                    logger.debug(pprint.pformat(player_api_dict))
                    logger.debug(f'player_api_dict[{key}]')
                    logger.debug(pprint.pformat(player_api_dict[key]))
                    input('...')

        try:
            self.save()
        except django.db.utils.DataError as e:
            logger.error(e)
            logger.error(self)
            input('...')

        return self

    def refresh_friendships(self):

        logger.debug(f'<SteamUser({self.steamid!r}, {self.personaname!r})>.refresh_friendships()')

        url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'  # ISteamUser GetFriendList
        payload = {
            'key': settings.STEAM_API_KEY,
            'steamid': self.steamid
            #'relationship' : 'friend'
        }
        r = requests.get(url, params=payload)

        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error(f'Request error on get_steam_friends for {self.steamid}')
            logger.error(e)
            self.friendships_are_public = False
            self.save()
            return

        # should we remove all friends here to remove old friendships?
        rj = r.json()

        steamid_list = []

        with Bar('Adding Friendships...') as bar:
            for friend in rj['friendslist']['friends']:
                friend_steamid = int(friend['steamid'])
                steamid_list.append(friend_steamid)
                friendObject, created = SteamUser.objects.get_or_create(steamid=friend_steamid)
                
                # Kan ikke refreshe alle venner bare fordi man trenger freidnship updates.
                # if created is True:
                #     friendObject.refresh_summary()
                #     friendObject.save()

                # logger.debug('Adding Friendship')
                self.add_friendship(friendObject, timezone.make_aware(dt.datetime.fromtimestamp(friend['friend_since'])), friend['relationship'])
                # logger.debug('Added Friendship')

                bar.next()

        self.friendships_updated = timezone.now()
        self.save()

        return self.get_friendships()

    def refresh_steam_games(self):

        logger.debug(f'<SteamUser({self.steamid!r}, {self.personaname!r})>.refresh_steam_games()')
        from .steam_game import SteamGame
        url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'  # ISteamUser GetOwnedGames
        payload = {
            'key': settings.STEAM_API_KEY,
            'steamid': self.steamid,
            'include_appinfo': 1,
            'include_played_free_games': 1,
            'format': 'json'
        }
        r = requests.get(url, params=payload)
        # r.raise_for_status()
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error('request for games failed.')

        rj = None
        try:
            rj = r.json()
        except Exception as e:
            logger.error(e)
            logger.error(f'payload: {payload}')
            logger.error(r.text)
        
        if rj is None:
            return

        # pprint(rj)
        game_appid_list = []
        if not 'games' in rj['response']:
            return

        with transaction.atomic():
            for game in rj['response']['games']:
                # logger.debug(f'{game=}')
                # logger.debug('update or create')
                app, created = SteamGame.objects.update_or_create(appid=game['appid'], defaults=dict(
                            name = game['name'],
                            icon_url = game['img_icon_url'],
                            # logo_url = game['img_logo_url']
                ))
                # logger.debug(f'{created=}')
                # logger.debug('app')
                # logger.debug(app)

                self.games.add(app)

        return self.games

    def add_friendship(self, steamuser: 'SteamUser', friends_since: dt.datetime, relationship: str, symm:bool=True):
        from . import Friendship
        friendship, created = Friendship.objects.get_or_create(
            from_steamuser=self,
            to_steamuser=steamuser,
            friends_since=friends_since,
            relationship=relationship)
        if symm:
            # avoid recursion by passing `symm=False`
            steamuser.add_friendship(self, friends_since, relationship, symm=False)
        return relationship

    def remove_friendship(self, steamuser, symm=True):
        from . import Friendship
        Friendship.objects.filter(
            from_steamuser=self,
            to_steamuser=steamuser,
            ).delete()
        if symm:
            # avoid recursion by passing `symm=False`
            steamuser.remove_friendship(self, symm=False)

    def get_friendships(self):
        return self.friendships.filter(
            to_steamusers__from_steamuser=self)

    def __str__(self):
        return f'{self.personaname} ({self.steamid})'
                # {self.profileurl!r}, \n\
                # {self.avatar!r}, \n\
                # {self.avatarmedium!r}, \n\
                # {self.avatarfull!r}, \n\
                # {self.personastate!r}, \n\
                # {self.communityvisibilitystate!r}, \n\
                # {self.profilestate!r}, \n\
                # {self.lastlogoff!r}, \n\
                # {self.commentpermission!r}\n\
                # \n\
                # {self.realname!r}\n\
                # {self.primaryclanid!r}\n\
                # {self.timecreated!r}\n\
