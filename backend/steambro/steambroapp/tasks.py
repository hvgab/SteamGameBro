

from celery import shared_task
from .utils import sync_player as utils_sync_player

@shared_task
def sync_player(args*, kwargs**):
    utils_sync_player(args*, kwargs**)
