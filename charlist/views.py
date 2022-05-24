# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, reverse

from .flyweights import *
from .constants import *


import json


aptitudes = Aptitude.from_file(json.load(open('static/json/aptitudes.json', 'r', encoding='utf-8')))
stat_descriptions = StatDescription.from_file(json.load(open('static/json/stat_descriptions.json',
                                                             'r', encoding='utf-8')))


def aptitudes_test(request):
    logger = logging.getLogger('charlist_logger')
    logger.info('test')
    return render(request, 'charlist_test.html', {'version': VERSION, 'apts': aptitudes,
                                                  'stdescrs': stat_descriptions,})


def charsheet_mockup(request):
    return render(request, 'charsheet-mockup.html', {'version': VERSION, })
