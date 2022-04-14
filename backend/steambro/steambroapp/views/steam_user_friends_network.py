from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from steamlib import SteamUser as SteamUserAPI
from ..models import SteamUser
from ..models import SteamGame
from pprint import pprint, pformat
import json
import logging

log = logging.getLogger(__name__)

# Create your views here.
class SteamUserFriendsNetworkView(ListView):
    model = SteamUser
    template_name = 'steambroapp/steamuser_friends_network.html'

    def get_queryset(self):
        steam_user_pk = self.kwargs['pk']
        steam_user = SteamUser.objects.get(id=steam_user_pk)
        friends = steam_user.friendships.all()
        return friends

    def get_context_data(self, **kwargs):
        # update user
        context = super().get_context_data(**kwargs)
        context["friends"] = list(self.get_queryset())
        friends_json = [{'id':friend.id, 'steam_id':friend.steamid, 'personaname': friend.personaname, 'label': f'{friend.id}-{friend.personaname}', 'friends':[ff.id for ff in friend.friendships.all()]} for friend in context['friends']]
        context["friends_json"] = friends_json
        
        steam_user_pk = self.kwargs['pk']
        steam_user = SteamUser.objects.get(id=steam_user_pk)
        context['steam_user'] = steam_user
        context["steam_user_json"] = {'id':steam_user.id, 'steam_id':steam_user.steamid, 'personaname': steam_user.personaname}
        return context
    



