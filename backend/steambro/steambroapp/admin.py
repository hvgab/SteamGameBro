from django.contrib import admin
from .models import SteamUser, SteamGame, Friendship
# Register your models here.
from . import service

@admin.register(SteamUser)
class SteamUserAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'steamid', 'personaname', 'realname']
    list_filter = [('personaname', admin.BooleanFieldListFilter)]
    search_fields = ['steamid', 'personaname']

    @admin.action(description='Refresh Steam User Summary')
    def refresh_player_summaries(modeladmin, request, queryset):
        for steam_user in queryset:
            service.refresh_steam_user_summary(steam_user)

    @admin.action(description='Refresh Friends List')
    def refresh_friends_list(modeladmin, request, queryset):
        for steam_user in queryset:
            service.refresh_steam_user_friends_list(steam_user)
            

    actions = ['refresh_player_summaries', 'refresh_friends_list']

@admin.register(SteamGame)
class SteamGameAdmin(admin.ModelAdmin):
    pass

@admin.register(Friendship)
class SteamFriendshipAdmin(admin.ModelAdmin):
    pass
