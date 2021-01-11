from django.contrib import admin
from .models import SteamUser, SteamGame
# Register your models here.
admin.site.register(SteamUser)
admin.site.register(SteamGame)
