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


log = logging.getLogger(__name__)

# Create your views here.
class SteamUserFriendsNetworkView(TemplateView):
    template_name = 'steambroapp/steamuser_friends_network.html'

    def get_context_data(self, **kwargs):
        # update user

        context = super().get_context_data(**kwargs)

        # Get user
        steam_user_pk = self.kwargs['pk']
        steam_user = SteamUser.objects.get(id=steam_user_pk)

        steam_user.refresh_summary()
        steam_user.refresh_friendships()

        # Get friends
        friends = steam_user.friendships.all()

        context["friends"] = list(friends)

        # user list for json-script
        users_list = []
        for user in friends:
            users_list.append(
                {
                    'id': user.id, 
                    'steam_id': user.steamid,
                    'primaryclan': user.primaryclanid,
                    'name': user.personaname, 
                    'x': random.random(),
                    'y': random.random(), 
                    'size': 5,
                    'label': f'{user.id}-{user.personaname}',
                    'color': "blue",
                }
            )
        
        users_list.append(
            {
                'id': steam_user.id, 
                'steam_id': steam_user.steamid, 
                'name': steam_user.personaname, 
                'x': random.random(),
                'y': random.random(), 
                'size': 5,
                'label': f'{steam_user.id}-{steam_user.personaname}',
                'color': "blue",
            }
        )

        # user list to filter friendships
        user_id_list = [u.id for u in friends]
        # friendships
        friendships = Friendship.objects.filter(from_steamuser_id__in=user_id_list, to_steamuser_id__in=user_id_list)
        friendship_list = []
        for f in friendships:
            friendship_list.append({'source': f.from_steamuser_id, 'target': f.to_steamuser_id})

        context["friends"] = users_list
        context["friendships"] = friendship_list

        context['steam_user'] = steam_user

        return context
    



