
from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import IndexView, LogoutView

app_name = 'account'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path(
        'logout',
        login_required(LogoutView.as_view(), login_url='/'),
        name='logout')
]
