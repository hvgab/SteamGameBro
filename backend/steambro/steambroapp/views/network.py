from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from ..models.steam_user_friendship import Friendship
from steamlib import SteamUser as SteamUserAPI
from ..models import SteamUser, Friendship
from ..models import SteamGame
from pprint import pprint, pformat
import json
import logging

log = logging.getLogger(__name__)

# Create your views here.
class NetworkView(TemplateView):
    template_name = 'steambroapp/network.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # log.debug('getting users')
        # users = SteamUser.objects.order_by('-id').all()[:1000]
        # users_ids = [u.id for u in users]
        
        # log.debug('getting friendships')
        # friendships = Friendship.objects.filter(from_steamuser__in=users, to_steamuser__in=users).all()
        # log.debug(pformat(friendships))

        log.debug('getting friendships')
        friendships = Friendship.objects.order_by('id').all()[:1000]
        # log.debug(pformat(friendships))  

        from_friendship_user_ids = friendships.values_list('from_steamuser_id', flat=True)
        to_friendship_user_ids = friendships.values_list('to_steamuser_id', flat=True)
        friendship_user_ids = set(list(from_friendship_user_ids)+list(to_friendship_user_ids))
        log.debug(pformat(friendship_user_ids))

        log.debug('getting users')
        users = SteamUser.objects.filter(id__in=friendship_user_ids).order_by('-id').all()
        users_ids = [u.id for u in users]
        log.debug(pformat(users_ids))

        log.debug('making user list')
        users_list = []
        for user in users:
            users_list.append({'id': user.id, 'steam_id': user.steamid, 'name': user.personaname, 'label': f'{user.id}-{user.personaname}'})
        # log.debug(pformat(users_list))

        log.debug('making friendship list')
        friendship_list = []
        for f in friendships:
            friendship_list.append({'from': f.from_steamuser.id, 'to': f.to_steamuser.id})
        # log.debug(pformat(friendship_list))
        
        log.debug('adding to context')
        # context['users'] = users
        context['users_list'] = users_list
        # context['friendships'] = friendships
        context['friendships_list'] = friendship_list
        return context
    



