from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from ..models.steam_user_friendship import Friendship
from steamlib import SteamUser as SteamUserAPI
from ..models import SteamUser
from ..models import SteamGame
from pprint import pprint, pformat
import json
import logging
import random 
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


logger = logging.getLogger(__name__)

# Create your views here.
class SteamUserFriendsNetworkView(TemplateView):
    template_name = 'steambroapp/steamuser_friends_network.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        include_self = self.request.GET.get('include_self', 0)
        logger.debug(f'{include_self=}')
        include_self = bool(int(self.request.GET.get('include_self', 0)))
        logger.debug(f'{include_self=}')

        # Get user
        steam_user_pk = self.kwargs['pk']
        steam_user = SteamUser.objects.get(id=steam_user_pk)

        a_week_ago = timezone.now() + timedelta(weeks=-1)
        if (steam_user.summary_updated is None or steam_user.summary_updated < a_week_ago):
            steam_user.refresh_summary()
        
        if (steam_user.friendships_updated is None or steam_user.friendships_updated < a_week_ago):
            steam_user.refresh_friendships()
        

        logger.debug(f'{steam_user}')
        logger.debug(f'{steam_user.friendships_updated}')
        logger.debug(f'{steam_user.friendships_are_public}')

        # Get friends
        friends = steam_user.friendships.all()

        logger.debug(f'{timezone.now()=}')
        logger.debug(f'{a_week_ago=}')
        
        friend_i = 0
        friend_len = len(friends)
        for friend in friends:
            friend_i += 1
            # logger.debug(f'{friend}')
            if friend_i % 10 == 0:
                logger.debug(f'Friends loop: {friend_i} / {friend_len}')
            if friend.friendships_are_public is False:
                # logger.debug(f'Skipping {friend}, friends are not public')
                continue
            if ((friend.friendships_updated is not None) and (friend.friendships_updated > a_week_ago)):
                # logger.debug(f'Skipping {friend}, friends are recent enough ({friend.friendships_updated})')
                continue
            # logger.debug(f'friendships is public: {friend.friendships_are_public}')
            # logger.debug(f'friendships ever updated: {friend.friendships_updated is not None}')
            if friend.friendships_updated is not None:
                # logger.debug(f'friendships are updated before a week ago: {friend.friendships_updated>a_week_ago}')
                pass
            friend.refresh_friendships()

        context["friends"] = list(friends)

        # user list for json-script
        users_list = []
        for user in friends:
            users_list.append(
                {
                    'id': user.id, 
                    'steam_id': user.steamid,
                    'primaryclan': user.primaryclanid,
                    'personaname': user.personaname, 
                    'x': random.random(),
                    'y': random.random(), 
                    'size': 5,
                    'label': f'{user.id}-{user.personaname}',
                    'color': "#333",
                }
            )
        
        if include_self is True:
            users_list.append(
                {
                    'id': steam_user.id, 
                    'steam_id': steam_user.steamid, 
                    'primaryclan': user.primaryclanid,
                    'personaname': steam_user.personaname, 
                    'x': random.random(),
                    'y': random.random(), 
                    'size': 5,
                    'label': f'{steam_user.id}-{steam_user.personaname}',
                    'color': "#333",
                }
            )

        # user list to filter friendships
        user_id_list = [u.id for u in friends]
        if include_self is True:
            user_id_list.append(steam_user_pk)

        # friendships
        friendships = Friendship.objects.filter(from_steamuser_id__in=user_id_list, to_steamuser_id__in=user_id_list)
        friendship_list = []
        for f in friendships:
            friendship_list.append({'source': f.from_steamuser_id, 'target': f.to_steamuser_id})

        context["friends"] = users_list
        context["friendships"] = friendship_list

        context['steam_user'] = steam_user
        context['watermark_json'] = {
            'name':steam_user.personaname, 
            'steamid':steam_user.steamid, 
            'steamurl': steam_user.profileurl,
            'avatar': steam_user.avatarmedium,
            }


        return context
    



