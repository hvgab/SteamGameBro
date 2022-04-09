from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from steamlib import SteamUser as SteamUserAPI
from ..models import SteamUser
from ..models import SteamGame
from pprint import pprint, pformat
import logging

log = logging.getLogger(__name__)

# Create your views here.
class SteamGameListView(ListView):
    model = SteamGame
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset()

class SteamGameDetailView(DetailView):
    model = SteamGame