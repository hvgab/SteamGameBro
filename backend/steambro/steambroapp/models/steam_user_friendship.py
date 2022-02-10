from django.db import models
from django.utils.translation import gettext_lazy as _

class Friendship(models.Model):
    """ Friendship between SteamUsers
        
        Don't create friendships here directly, use steam_user.add_friendship()
    """
    from_steamuser = models.ForeignKey("steambroapp.SteamUser", verbose_name="", on_delete=models.CASCADE, related_name='from_steamusers')
    to_steamuser = models.ForeignKey("steambroapp.SteamUser", verbose_name="", on_delete=models.CASCADE, related_name='to_steamusers')
    friends_since = models.DateTimeField(_("friends since"))
    relationship = models.CharField(_("relationship"), max_length=50)

    def __str__(self) -> str:
        return f'{self.from_steamuser} -> {self.to_steamuser}'