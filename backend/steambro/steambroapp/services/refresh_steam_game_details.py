from asyncio.log import logger
from django.conf import settings
from ..models import SteamGame
import logging
import requests
from pprint import pprint
from service_objects.services import Service
from service_objects import fields as service_fields
logger = logging.getLogger(__name__)

class RefreshSteamGameDetails(Service):
    steam_game = service_fields.ModelField(SteamGame)

    def process(self):

        steam_game = self.cleaned_data['steam_game']
        
        logger.debug(f'start api/appdetails service for {steam_game}')

        url = "https://store.steampowered.com/api/appdetails"
        params = {
            'appids':steam_game.appid,
            'l':'english',
        }

        # payload = {'key': settings.STEAM_API_KEY, 'steamids': steam_user.steamid}
        
        r = requests.get(url, params=params)

        try:
            rj = r.json()
        except Exception as e:
            raise ValueError('request error. \n{r.test}') 

        rj_keys = rj.keys()
        root_key = list(rj_keys)[0]

        logger.debug(rj[root_key]['success'])
        if rj[root_key]['success'] == False:
            return

        try:
            steam_game.detailed_description = rj[root_key]['data']['detailed_description']
        except KeyError as e:
            logger.error(e)
        steam_game.about_the_game = rj[root_key]['data']['about_the_game']
        steam_game.short_description = rj[root_key]['data']['short_description']
        steam_game.header_url = rj[root_key]['data']['header_image']
        steam_game.background_url = rj[root_key]['data']['background']

        steam_game.save()
        
        # steam_game.website = rj['data']['website']
        # steam_game.developers = rj['data']['website']
        # steam_game.publishers = rj['data']['website']
        # steam_game.categories = rj['data']['website']
        # steam_game.genres = rj['data']['website']
        # steam_game.screenshots = rj['data']['website']
        # steam_game.movies = rj['data']['website']
        # steam_game.achievements = rj['data']['website']
        # steam_game.release_date = rj['data']['website']
        # steam_game.release_date = rj['data']['website']