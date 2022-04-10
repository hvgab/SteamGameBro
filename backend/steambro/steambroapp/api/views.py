from rest_framework import viewsets
from .serializers import SteamUserSerializer, SteamGameSerializer, UserGameGroupSerializer
from ..models import SteamUser, SteamGame, UserGameGroup

class SteamGameViewSet(viewsets.ModelViewSet):
    queryset = SteamGame.objects.all()
    serializer_class = SteamGameSerializer

class SteamUserViewSet(viewsets.ModelViewSet):
    queryset = SteamUser.objects.all()
    serializer_class = SteamUserSerializer

class UserGameGroupViewSet(viewsets.ModelViewSet):
    queryset = UserGameGroup.objects.all()
    serializer_class = UserGameGroupSerializer
