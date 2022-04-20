from django.db import models
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File

class UserGameGroup(models.Model):
    user = models.ForeignKey(to='SteamUser', on_delete=models.CASCADE)
    game = models.ForeignKey(to='SteamGame', on_delete=models.CASCADE)
    group = models.ForeignKey(to='GameGroup', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                 fields=['user', 'game', 'group'], 
                 name='unique_user_game_group'
            )
    ]

    def __repr__(self):
        return f'<UserGameGroup({self.id}, user={self.user!r}, game={self.game!r}, group={self.group!r})>'

    def __str__(self):
        return f'{self.user} + {self.game} + {self.group}'

