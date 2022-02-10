from rest_framework import viewsets
from .serializers import SteamUserSerializer, SteamGameSerializer
from ..models import SteamUser, SteamGame

class SteamGameViewSet(viewsets.ModelViewSet):
    queryset = SteamGame.objects.all()
    serializer_class = SteamGameSerializer

class SteamUserViewSet(viewsets.ModelViewSet):
    queryset = SteamUser.objects.all()
    serializer_class = SteamUserSerializer
