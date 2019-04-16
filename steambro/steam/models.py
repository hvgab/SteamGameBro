from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from steamlib import SteamGame as SteamGameAPI
from steamlib import SteamUser as SteamUserAPI
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


class SteamUserManager(models.Manager):
    def get_or_api(self, **kwargs):
        print('steamusermanager - get')
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            # print('**kwargs')
            # print(**kwargs)
            print('kwargs')
            print(kwargs)

            try:
                steamUser = SteamUserAPI(kwargs['steamid'])
                steamUser.getPlayerSummaries()

                instance = SteamUser(
                    steamid=steamUser.steamid,
                    personaname=steamUser.personaname,
                    profileurl=steamUser.profileurl,
                    avatar=steamUser.avatar,
                    avatarmedium=steamUser.avatarmedium,
                    avatarfull=steamUser.avatarfull)

                instance.save()
                return instance
            except Exception as e:
                raise

        except Exception as e:
            print('unknwokn err')
            raise e


class SteamUser(models.Model, SteamUserAPI):
    steamid = models.BigIntegerField()
    personaname = models.CharField(max_length=255)
    profileurl = models.CharField(max_length=500)
    avatar = models.CharField(max_length=500)
    avatarmedium = models.CharField(max_length=500)
    avatarfull = models.CharField(max_length=500)
    last_update = models.DateTimeField(auto_now=True)
    ownedGames = models.CharField(
        max_length=1000000,
        blank=True,
        validators=[validate_comma_separated_integer_list])
    friends = models.ManyToManyField('SteamUser')  #, through='Friendship')

    manager = SteamUserManager()

    def getFriends(self):
        friendlist = self.getFriendList()
        print(friendlist)


# class Friendship(models.Model):


class SteamGameMangager(models.Manager):
    def get_or_api(self, **kwargs):
        pass


class SteamGame(models.Model):
    # Base App Info
    appid = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    img_icon_url = models.CharField(max_length=500)
    img_icon = models.ImageField(upload_to='SteamGame')
    img_logo_url = models.CharField(max_length=500)
    img_logo = models.ImageField(upload_to='SteamGame')
    # Detailed App Info:
    has_detailed_info = models.BooleanField(default=False)

    # False,
    # help_text='If this is false, an API request to app api will be made.')

    def __repr__(self):
        return f'<SteamGame({self.appid}, name={self.name!r})>'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Overwrite default save function."""
        self.get_remote_image()
        super(SteamGame, self).save(*args, **kwargs)

    def get_remote_image(self):
        IMG_ICON_URL = f'http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.img_icon_url}.jpg'
        IMG_LOGO_URL = f'http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{self.img_logo_url}.jpg'
        if self.img_icon_url and not self.img_icon:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(IMG_ICON_URL).read())
            img_temp.flush()
            self.img_icon.save(f'{self.appid}_img_icon', File(img_temp))

        if self.img_logo_url and not self.img_logo:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(IMG_LOGO_URL).read())
            img_temp.flush()
            self.img_logo.save(f'{self.appid}_img_logo', File(img_temp))

        # self.save()
