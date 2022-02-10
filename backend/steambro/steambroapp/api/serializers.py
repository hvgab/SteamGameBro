from rest_framework import serializers
from ..models import SteamGame, SteamUser

class SteamGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamGame
        fields = '__all__'

class SteamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamUser
        fields = '__all__'
