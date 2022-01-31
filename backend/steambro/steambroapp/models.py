from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from steamlib import SteamGame as SteamGameAPI
from steamlib import SteamUser as SteamUserAPI
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
import logging
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import requests
import json
from django.utils import timezone
import datetime as dt
from pprint import pprint
import django

log = logging.getLogger(__name__)


class SteamUserManager(models.Manager):
    def get_or_api(self, steamid):
        try:
            return super().get_queryset().get(steamid=steamid)
        except ObjectDoesNotExist:
            log.error(f'Object does not exist with steamid: {steamid}')

            try:
                log.debug('steamuser api')
                steamUser_api = SteamUserAPI(steamid)
                log.debug('get player summaries')
                steamUser_api.getPlayerSummaries()
                log.debug('got player summaries')

                log.debug('creating instance')
                instance = SteamUser(
                    steamid=steamUser_api.steamid,
                    personaname=steamUser_api.personaname,
                    profileurl=steamUser_api.profileurl,
                    avatar=steamUser_api.avatar,
                    avatarmedium=steamUser_api.avatarmedium,
                    avatarfull=steamUser_api.avatarfull)
                log.debug('instance created')

                log.debug('saving instance')
                instance.save()
                log.debug('instance saved')
                return instance
            except Exception as e:
                raise

        except Exception as e:
            log.exception('Unknown Error')


class SteamUser(models.Model):
    ## Public Data
    
    # steamid - 64bit SteamID of the user
    steamid = models.BigIntegerField(unique=True)
    steamid_text = models.CharField(max_length=255, blank=True, null=True)
    
    # personaname
    # The player's persona name (display name)
    personaname = models.CharField(max_length=255)
    
    # profileurl
    # The full URL of the player's Steam Community profile.
    profileurl = models.CharField(max_length=500)
    
    # avatar
    # The full URL of the player's 32x32px avatar. 
    # If the user hasn't configured an avatar, this will be the default ? avatar.
    avatar = models.CharField(max_length=500)
    
    # avatarmedium
    # The full URL of the player's 64x64px avatar. 
    # If the user hasn't configured an avatar, this will be the default ? avatar.
    avatarmedium = models.CharField(max_length=500)
    
    # avatarfull
    # The full URL of the player's 184x184px avatar. 
    # If the user hasn't configured an avatar, this will be the default ? avatar.
    avatarfull = models.CharField(max_length=500)
    
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
    
    # loccountrycode
    # If set on the user's Steam Community profile, The user's country of residence, 2-character ISO country code
    
    # locstatecode
    # If set on the user's Steam Community profile, The user's state of residence
    
    # loccityid
    # An internal code indicating the user's city of residence. A future update will provide this data in a more useful way.
    # steam_location gem/package makes player location data readable for output.


    owned_games_list = models.CharField(
        max_length=1000000,
        blank=True,
        validators=[validate_comma_separated_integer_list])
    
    games = models.ManyToManyField("steambroapp.SteamGame", verbose_name=_("games"))
    friends = models.ManyToManyField('self', verbose_name=_("friends"), through='Friendship', symmetrical=True)

    # SteamBro
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(_("created at"), auto_now=False, auto_now_add=True)
    objects = models.Manager()  # Default manager
    manager = SteamUserManager()  # Custom manager

    def update_steam_player_summary(self):
        log.debug(f'update user with steamid {self.steamid!r}')
        url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'  # ISteamUser_GetPlayerSummaries
        payload = {'key': settings.STEAM_API_KEY, 'steamids': self.steamid}
        r = requests.get(url, params=payload)
        
        try:
            rj = r.json()
        except json.decoder.JSONDecodeError as e:
            log.error(f'Json Decode Error on update steam player summary for {self.steamid}')
            return


        # Get Data
        player_api_dict = rj['response']['players'][0]
        # Get Public Data
        fields_as_int = ['personastate', 'communityvisibilitystate', 'profilestate', 'commentpermission', 'primaryclanid']
        fields_unix_to_datetime = ['lastlogoff', 'timecreated']

        log.info(f'updateing db from api for user {self.steamid}')
        for key in player_api_dict.keys():
            if (key in self.__dict__.keys()) and (key in player_api_dict.keys()):
                if key in fields_as_int:
                    setattr(self, key, int(player_api_dict[key]))
                elif key in fields_unix_to_datetime:
                    setattr(self, key, timezone.make_aware(dt.datetime.fromtimestamp(player_api_dict[key])))
                else:
                    setattr(self, key, player_api_dict[key])
            else:
                log.warning(f'Key {key.upper()} not in class attributes')

        try:
            self.save()
        except django.db.utils.DataError as e:
            log.error(e)
            log.error(self)
            input('...')

    def get_steam_friends(self):
        url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'  # ISteamUser GetFriendList
        payload = {
            'key': settings.STEAM_API_KEY,
            'steamid': self.steamid
            #'relationship' : 'friend'
        }
        r = requests.get(url, params=payload)

        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            log.error(f'Request error on get_steam_friends for {self.steamid}')
            return

        rj = r.json()

        steamid_list = []
        for friend in rj['friendslist']['friends']:
            # log.debug(friend)
            friend_steamid = int(friend['steamid'])
            steamid_list.append(friend_steamid)
            if SteamUser.objects.filter(steamid=friend_steamid).count() <= 0:
                friendObject, created = SteamUser.objects.get_or_create(steamid=friend_steamid)
                if created is True:
                    friendObject.update_steam_player_summary()
                    friendObject.save()

            # TODO: Save as friends here?
        
        friendlist = SteamUser.objects.filter(steamid__in=steamid_list).all()
        return friendlist

    def get_steam_games(self):
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
            log.error('request for games failed.')

        rj = None
        try:
            rj = r.json()
        except Exception as e:
            log.debug(e)
            log.debug(f'payload: {payload}')
            log.debug(r.text)
            result = None
        
        if rj is None:
            return

        # pprint(rj)
        game_appid_list = []
        if not 'games' in rj['response']:
            return

        for game in rj['response']['games']:
            game_appid_list.append(game['appid'])
            if SteamGame.objects.filter(appid=game['appid']).count() <= 0:
                game_object = SteamGame(
                        appid = game['appid'],
                        name = game['name'],
                        icon_url = game['img_icon_url'],
                        logo_url = game['img_logo_url']
                )
                game_object.save()

        return SteamGame.objects.filter(appid__in=game_appid_list).all()

    def __str__(self):
        return f'SteamUser<{self.steamid!r}, personaname={self.personaname!r}>'
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


class Friendship(models.Model):
    from_steamuser_id = models.ForeignKey("steambroapp.SteamUser", verbose_name=_(""), on_delete=models.CASCADE, related_name='origin_friend')
    to_steamuser_id = models.ForeignKey("steambroapp.SteamUser", verbose_name=_(""), on_delete=models.CASCADE, related_name='friend_origin')
    friend_since = models.DateTimeField(_("friends since"), auto_now=False, auto_now_add=False)
    relationship = models.CharField(_("relationship"), max_length=50)


class SteamGameMangager(models.Manager):
    def get_or_api(self, **kwargs):
        pass


class SteamGame(models.Model):
    # Base App Info
    appid = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    
    # IMG
    icon_url = models.CharField(max_length=500, blank=True, null=True)
    icon = models.ImageField(upload_to='SteamGame', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    logo_url = models.CharField(max_length=500, blank=True, null=True)
    logo = models.ImageField(upload_to='SteamGame', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    header_url = models.CharField(max_length=500, blank=True, null=True)
    header = models.ImageField(upload_to='SteamGame', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    background_url = models.CharField(max_length=500, blank=True, null=True)
    background = models.ImageField(upload_to='SteamGame', height_field=None, width_field=None, max_length=None, blank=True, null=True)

    # Detailed App Info:
    has_detailed_info = models.BooleanField(default=False)
    detailed_description = models.TextField(blank=True, null=True)
    about_the_game = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)

    # Webapp fields
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __repr__(self):
        return f'<SteamGame({self.appid}, name={self.name!r})>'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Overwrite default save function."""
        self.get_remote_image()
        super(SteamGame, self).save(*args, **kwargs)

    def get_remote_image(self):
        IMG_ICON_URL = f'http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.icon_url}.jpg'
        IMG_LOGO_URL = f'http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.logo_url}.jpg'
        if self.icon_url and not self.icon:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(IMG_ICON_URL).read())
            img_temp.flush()
            self.icon.save(f'{self.appid}_icon', File(img_temp))

        if self.logo_url and not self.logo:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(IMG_LOGO_URL).read())
            img_temp.flush()
            self.logo.save(f'{self.appid}_logo', File(img_temp))

        # self.save()
