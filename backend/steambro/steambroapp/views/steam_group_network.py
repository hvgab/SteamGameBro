from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from ..models.steam_user_friendship import Friendship
from steamlib import SteamUser as SteamUserAPI
from steamlib import SteamGroup as SteamGroupAPI
from ..models import SteamUser
from ..models import SteamGame
from pprint import pprint, pformat
import json
import logging
import random 
from django.db.models import Q
from progress.bar import Bar
from django.utils import timezone
from datetime import timedelta


logger = logging.getLogger(__name__)

# Create your views here.
class SteamGroupNetworkView(TemplateView):
    template_name = 'steambroapp/steamgroup_network.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get Group Members
        group_id = self.kwargs['groupID64']
        groupAPI = SteamGroupAPI(group_id)
        members = groupAPI.get_members_list()

        user_id_list = []
        user_list = []
        friendship_list = []

        with Bar('Getting members...') as bar:
            i = 0
            members_length = len(members)
            for member in members:
                i += 1
                logger.info(f'== {i} / {members_length} ==')
                steam_user, created = SteamUser.objects.get_or_create(steamid=member)
                # logger.debug(f'{created=}')
                # logger.debug(f'{steam_user=}')

                if created is True:
                    steam_user.refresh_summary()

                # update friendships if
                a_week_ago = timezone.now() + timedelta(weeks=-1)
                if (
                    steam_user.friendships_are_public != False 
                    and (steam_user.friendships_updated is None or steam_user.friendships_updated < a_week_ago)
                    ):
                    steam_user.refresh_friendships()

                logger.debug(f'{steam_user.id} - {steam_user.primaryclanid}')
                user_list.append(
                    {
                        'id': steam_user.id,
                        'primaryclanid': str(steam_user.primaryclanid),
                        'label': f'{steam_user.id} - {steam_user.personaname}',
                        'x': random.random(),
                        'y': random.random(),
                        'color': 'blue',
                        'size': 5,
                        # 'type': "image", 
                        # 'image': steam_user.avatar,
                    }
                )
                user_id_list.append(steam_user.id)

                bar.next()

        # Get friendships
        friendships = Friendship.objects.filter(from_steamuser_id__in=user_id_list, to_steamuser_id__in=user_id_list)
        for fs in friendships:
            friendship_list.append(
                {
                    'source': fs.from_steamuser_id,
                    'target': fs.to_steamuser_id,
                }
            )

        context["friends"] = user_list
        context["friendships"] = friendship_list

        return context
    



