from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from backend.steambro.steamlib.group import SteamGroup
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
class SteamGroupListView(ListView):
    template_name = 'steambroapp/steamgroup_list.html'
    model = SteamGroup

class SteamGroupDetailView(DetailView):
    template_name = 'steambroapp/steamgroup_detail.html'
    model = SteamGroup
    
    



