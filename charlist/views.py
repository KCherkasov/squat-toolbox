# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, reverse

from .flyweights import *
from .constants import *


resources = ['aptitudes.json', 'stat_descriptions.json', 'skill_descriptions.json']
flyweights = Facade(resources)


def aptitudes_test(request):
    logger = logging.getLogger('charlist_logger')
    logger.info('test')
    return render(request, 'charlist_test.html', {'version': VERSION, 'facade': flyweights, })


def charsheet_mockup(request):
    return render(request, 'charsheet-mockup.html', {'version': VERSION, })
