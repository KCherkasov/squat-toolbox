# -*- coding: utf-8 -*-

from django.contrib import admin
from charlist import models

admin.site.register(models.CharsheetUser)
admin.site.register(models.Character)
admin.site.register(models.RTCreationData)
admin.site.register(models.CreationData)
admin.site.register(models.Season)

admin.register(models.CharacterGroup)
