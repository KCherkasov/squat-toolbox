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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from charlist import rt_views
from charlist import views as charviews
from namegen import views, settings

urlpatterns = [
    path(r'', views.main, name='main'),
    path(r'admin/', admin.site.urls),
    path(r'namegen/', views.namegen, name='namegen'),

    path(r'signup/', charviews.signup, name='signup'),
    path(r'signin/', charviews.signin, name='signin'),
    path(r'signout/', charviews.logout, name='logout'),
    path(r'activate/<str:uidb64>/<str:token>/',
         charviews.activate, name='activate'),
    path(r'activate-pending/', charviews.signup_activate, name='signup-activate'),

    path(r'characters/', charviews.characters_list, name='characters-list'),

    path(r'create-new-character/', charviews.create_character_start, name='create-character-start'),
    path(r'create-character/init/<int:creation_id>/', charviews.create_character_init,
         name='create-character-init'),
    path(r'create-character/hw-choice/<int:creation_id>/', charviews.create_character_hw_choice,
         name='create-character-hw'),
    path(r'create-character/characteristics/<int:creation_id>/', charviews.create_character_stat_distribution,
         name='create-character-stats'),
    path(r'create-character/bg-choice/<int:creation_id>/', charviews.create_character_bg_choice,
         name='create-character-bg'),
    path(r'create-character/role-choice/<int:creation_id>/', charviews.create_character_role_choice,
         name='create-character-role'),
    path(r'create-character/choices/<int:creation_id>/', charviews.create_character_choices,
         name='create-character-choice'),
                  path(r'create-character/rep-apts/<int:creation_id>/', charviews.create_character_double_apts,
                       name='create-character-double-apts'),
    path(r'create-character/divination/<int:creation_id>/', charviews.create_character_divination,
         name='create-character-divination'),

    path(r'create-new-rt-character/', rt_views.create_character_rt_start,
         name='create-character-rt-start'),
    path(r'create-character-rt/init/<int:creation_id>/',
         rt_views.rt_create_character_init, name='rt-create-character-init'),
    path(r'create-character-rt/origin-and-career/<int:creation_id>/',
         rt_views.rt_create_character_oac_choice, name='rt-create-character-oac'),
    path(r'create-character-rt/characteristics/<int:creation_id>/',
         rt_views.rt_create_character_stat_distribution, name='rt-create-character-stats'),
    path(r'create-character-rt/choices/<int:creation_id>/', rt_views.rt_create_character_choices,
         name='rt-create-character-choices'),
    path(r'create-character-rt/rep-apts/<int:creation_id>/', rt_views.create_character_double_apts,
         name='rt-create-character-double-apts'),
    path(r'create-character-rt/divination/<int:creation_id>/', rt_views.create_character_divination,
         name='rt-create-character-divination'),

    path(r'character/<int:char_id>/', charviews.character_view, name='character-details'),
    path(r'character/<int:char_id>/delete', charviews.character_delete, name='character-delete'),
    path(r'character/<int:char_id>/upgrade', charviews.character_upgrade, name='character-upgrade'),
    path(r'character/<int:char_id>/processing', rt_views.upg_midlayer, name='character-upg-midlayer'),
    path(r'character/<int:char_id>/sessions', charviews.character_sessions_list, name='sessions-list-char'),
    path(r'character/<int:char_id>/groups', charviews.groups_list_character, name='groups-list-char'),

    path(r'master/campaigns', charviews.seasons_list, name='seasons-list'),
    path(r'master/campaign/create', charviews.create_season, name='create-season'),
    path(r'master/campaign/<str:season_id>', charviews.season_view, name='season'),
    path(r'master/campaign/<str:season_id>/edit', charviews.season_edit, name='edit-season'),
    path(r'master/campaign/<str:season_id>/delete', charviews.season_delete, name='delete-season'),

    path(r'master/group/create/<str:season_id>', charviews.create_group, name='create-group'),
    path(r'master/group/<str:group_id>', charviews.group_view, name='group'),
    path(r'master/group/<str:group_id>/edit', charviews.group_edit, name='edit-group'),
    path(r'master/group/<str:group_id>/delete', charviews.group_delete, name='delete-group'),
    path(r'master/group/<str:group_id>/create-session', charviews.create_session, name='create-session'),
    path(r'master/group/<str:group_id>/create-session-crossover', charviews.create_crossover_session,
         name='create-crossover-session'),
    path(r'master/session/<int:game_session_id>', charviews.session_view, name='session'),
    path(r'master/sessions', charviews.sessions_list_master, name='sessions-list'),

    path(r'creation-data/<int:creation_id>/',
         charviews.resume_creation_edit, name='char-data-edit'),
    path(r'creation-data/<int:creation_id>/delete',
         charviews.creation_data_delete, name='char-data-delete'),
    path(r'rt-creation-data/<int:creation_id>/',
         rt_views.resume_creation_edit, name='rt-char-data-edit'),
    path(r'rt-creation-data/<int:creation_id>/delete',
         rt_views.creation_data_delete, name='rt-char-data-delete'),

    path(r'charsheet/test/', charviews.aptitudes_test, name='charsheet-test'),
    path(r'charsheet/mockup/', charviews.charsheet_mockup, name='charsheet-mockup'),
    path(r'charsheet/mockup-interactive/', charviews.interactive_charsheet_mockup, name='interactive-mockup'),

    path('api/namegen/get', views.get_name),
    path('api/namegen/ver', views.get_namegen_version),
    path('api/namegen/help', views.get_namegen_help),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
