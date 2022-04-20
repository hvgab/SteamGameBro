from django.contrib import admin
from .models import SteamUser, SteamGame, Friendship, GameGroup, UserGameGroup
# from .models import SteamGroup
# Register your models here.
from . import services

@admin.register(SteamUser)
class SteamUserAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'steamid', 'personaname', 'realname']
    list_filter = [('personaname', admin.BooleanFieldListFilter)]
    search_fields = ['steamid', 'personaname']

    @admin.action(description='Refresh Steam User Summary')
    def refresh_player_summaries(modeladmin, request, queryset):
        for steam_user in queryset:
            services.refresh_steam_user_summary(steam_user)

    @admin.action(description='Refresh Friends List')
    def refresh_friends_list(modeladmin, request, queryset):
        for steam_user in queryset:
            services.refresh_steam_user_friends_list(steam_user)
            

    actions = ['refresh_player_summaries', 'refresh_friends_list']

@admin.register(SteamGame)
class SteamGameAdmin(admin.ModelAdmin):
    search_fields = ['id', 'appid', 'name']

@admin.register(Friendship)
class SteamFriendshipAdmin(admin.ModelAdmin):
    def from_steamuser_steamid(self, obj):
        return obj.from_steamuser.steamid
    from_steamuser_steamid.short_description = 'From_Steamuser_Steamid'

    def to_steamuser_steamid(self, obj):
        return obj.to_steamuser.steamid
    to_steamuser_steamid.short_description = 'To_Steamuser_Steamid'

    def from_steamuser_personaname(self, obj):
        return obj.from_steamuser.personaname
    from_steamuser_personaname.short_description = 'From_Steamuser_personaname'

    def to_steamuser_personaname(self, obj):
        return obj.to_steamuser.personaname
    to_steamuser_personaname.short_description = 'To_Steamuser_personaname'

    def from_steamuser_id(self, obj):
        return obj.from_steamuser.id
    from_steamuser_id.short_description = 'From_Steamuser_ID'

    def to_steamuser_id(self, obj):
        return obj.to_steamuser.id
    to_steamuser_id.short_description = 'To_Steamuser_id'

    list_display = [
        'from_steamuser_steamid', 
        'to_steamuser_steamid', 
        'from_steamuser_personaname', 
        'to_steamuser_personaname', 
        'from_steamuser_id', 
        'to_steamuser_id',
        ]
    search_fields = ['from_steamuser__steamid', 'to_steamuser__steamid', 'from_steamuser__id', 'to_steamuser__id']

@admin.register(GameGroup)
class GameGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(UserGameGroup)
class UserGameGroupAdmin(admin.ModelAdmin):
    ordering = ['user_id', 'game_id']

# @admin.register(SteamGroup)
# class SteamGroupAdmin(admin.ModelAdmin):
#     pass
