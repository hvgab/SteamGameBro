# from django.contrib.auth.views import logout
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from django.views import View


class IndexView(View):
    def get(self, request):
        return render(request, 'account.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('steambroapp:index')
