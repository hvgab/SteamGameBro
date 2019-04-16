class SteamGame(object):
    """docstring for SteamGame."""

    def __init__(self, appid):
        super(SteamGame, self).__init__()
        self.appid = appid

    def img_link(self, hash):
        return f'http://media.steampowered.com/steamcommunity/public/images/apps/{self.appid}/{hash}.jpg'
