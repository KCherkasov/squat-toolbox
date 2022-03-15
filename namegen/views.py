# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .methods import *

version = '1.12.1'


LANG_KEY = 'lang'
GENDER_KEY = 'gender'
NOBILITY_KEY = 'nobility'
COUNT_KEY = 'count'

NAMEGEN_APP_JSON_KEYS = [LANG_KEY, GENDER_KEY, NOBILITY_KEY, COUNT_KEY]


def main(request):
    return HttpResponseRedirect(reverse('index'))


def index(request):
    if request.method == 'POST':
        form = NamegenForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            gender = data['gender']
            lang = data['lang']
            nobility = data['nobility']
            count = data['count']
            names = create_names(lang, gender, nobility, count)

            return render(request, 'namegen.html', {'form': form, 'names': names, 'version': version, })
    else:
        form = NamegenForm()

        return render(request, 'namegen.html', {'form': form, 'version': version, })


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def get_name(request, format=None):
    err = ''
    err += validate_request_data(request.data, NAMEGEN_APP_JSON_KEYS)
    lang = request.data.get('lang', 'R')
    gender = request.data.get('gender', 'R')
    nobility = request.data.get('nobility', 'R')
    count = request.data.get('count', 1)
    if isinstance(count, str):
        if count.isdigit():
            count = int(count)
        else:
            if err != '':
                err += '; '
            err = 'names count must be an integer'
            count = 1
    extra_errs = validate_data(lang, gender, nobility, count)
    if err != '':
        err += '; ' + extra_errs
    else:
        err = extra_errs
    if err != '':
        return Response({'errors': err}, status=status.HTTP_400_BAD_REQUEST)
    json = {'names': create_names(lang, gender, nobility, count)}
    return Response(json, status.HTTP_200_OK)


@api_view(['GET'])
def get_namegen_version(request, format=None):
    json = {'app': 'namegen', 'version': version}
    return Response(json, status.HTTP_200_OK)


def validate_data(lang, gender, nobility, count):
    error = ''
    if lang not in LANG_IDS and lang != Constants.TECH and lang != Constants.RANDOM:
        error += 'unknown language ID'
    if gender != Constants.RANDOM and gender != Constants.MALE and gender != Constants.FEMALE:
        if error != '':
            error += '; '
        error += 'unknown gender ID'
    if nobility != Constants.RANDOM and nobility != Constants.NOBLE and nobility != Constants.SIMPLE:
        if error != '':
            error += '; '
        error += 'unknown nobility ID'
    if count < 1 or count > 50:
        if error != '':
            error += '; '
        error += 'names count out of limits'
    return error


def validate_request_data(data, allowed_keys):
    err = ''
    for k in data.keys():
        if k not in allowed_keys:
            if err != '':
                err += '; '
            err += 'unknown JSON field: ' + k
    return err
