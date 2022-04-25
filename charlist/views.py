# -*- coding: utf-8 -*-
import sys

from django.shortcuts import render, reverse
import logging

from .flyweights import *
from .constants import *

logger = logging.getLogger('django')
logger.info('reading apts')
data = json.load(open('static/json/aptitudes.json', 'r'))
logger.info('apts read, making apt objects from\n')
logger.info(data)

aptitudes = Aptitude.from_file(data)


def aptitudes_test(request):
    return render(request, 'charlist_test.html', {'version': VERSION, 'apts': aptitudes, })
