from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import IndexView, UserGameListView, UserFriendListView
from . import views

app_name = 'steam'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('user/gamelist', UserGameListView.as_view(), name='usergamelist'),
    path(
        'user/friendlist', UserFriendListView.as_view(),
        name='userfriendlist'),
    path('couch', views.couch_home, name='couch_home'),
]
