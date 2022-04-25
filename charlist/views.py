# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, reverse

from .flyweights import *
from .constants import *


import json


data = json.load(open('static/json/aptitudes.json', 'r', encoding='utf-8'))
apts = Aptitudes()
apts.from_file(data)


def aptitudes_test(request):
    logger = logging.getLogger('charlist_logger')
    logger.info('test')
    return render(request, 'charlist_test.html', {'version': VERSION, 'apts': apts.apts, })
