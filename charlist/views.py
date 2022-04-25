# -*- coding: utf-8 -*-
import logging
import sys

from django.shortcuts import render, reverse

from .flyweights import *
from .constants import *


import json


data = json.load(open('static/json/aptitudes.json', 'r', encoding='utf-8'))
apts = Aptitude.from_file(data)


def aptitudes_test(request):
    logger = logging.getLogger('charlist_logger')
    logger.info(apts)
    return render(request, 'charlist_test.html', {'version': VERSION, 'apts': apts, })
