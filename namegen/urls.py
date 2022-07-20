# -*- coding: utf-8 -*-
"""namegen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from . import views, settings
from charlist import views as charviews

urlpatterns = [
    path(r'', views.main, name='main'),
    path(r'admin/', admin.site.urls),
    path(r'namegen/', views.index, name='index'),

    path(r'dev/signup/', charviews.signup, name='signup'),
    path(r'dev/signin/', charviews.signin, name='signin'),
    path(r'dev/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         charviews.activate, name='activate'),

    path(r'dev/charsheet/test/', charviews.aptitudes_test, name='charsheet-test'),
    path(r'dev/charsheet/mockup/', charviews.charsheet_mockup, name='charsheet-mockup'),
    path(r'dev/charsheet/mockup-interactive/', charviews.interactive_charsheet_mockup, name='interactive-mockup'),

    path('api/namegen/get', views.get_name),
    path('api/namegen/ver', views.get_namegen_version),
    path('api/namegen/help', views.get_namegen_help),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
