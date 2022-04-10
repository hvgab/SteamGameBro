from rest_framework import serializers
from ..models import SteamGame, SteamUser, UserGameGroup

class SteamGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamGame
        fields = '__all__'

class SteamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamUser
        fields = '__all__'

class UserGameGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGameGroup
        fields = '__all__'
