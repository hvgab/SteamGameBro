"""steambroproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path(
        'admin/doc/', 
        include('django.contrib.admindocs.urls')),
    path(
        'admin/', 
        admin.site.urls),
    path(
        '', 
        include('steambroapp.urls', namespace='steambroapp'), 
        name='steambro'),
    path(
        'social/',
        include('social_django.urls', namespace='social'),
        name='social'),
    path(
        'account/',
        include('account.urls', namespace='account'),
        name='account'),
    path(
        'api-auth/', 
        include('rest_framework.urls', namespace='rest_framework')
        ),
]
    
    