# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


from django.views.decorators.clickjacking import xframe_options_sameorigin

from .methods import *

version = '1.13.2'

LANG_KEY = 'lang'
GENDER_KEY = 'gender'
NOBILITY_KEY = 'nobility'
COUNT_KEY = 'count'

APP_KEY = 'приложение'
VERSION_KEY = 'версия'
API_ROOT_KEY = 'корень API'
API_KEY = 'мeтоды API'
ERR_KEY = 'ошибки'

DESCRIPTION_KEY = 'описание'
TYPE_KEY = 'тип данных'
METHOD_KEY = 'метод запроса'
REQ_JSON_KEY = 'обязательные JSON-поля'
ALLOWED_JSON_KEY = 'опциональные JSON-поля'
RETURN_KEY = 'возвращаемое значение'

NAMEGEN_APP_JSON_KEYS = [LANG_KEY, GENDER_KEY, NOBILITY_KEY, COUNT_KEY]

FIELD_VALUES = {
    LANG_KEY: {
        TYPE_KEY: 'строка',
        Constants.RANDOM: 'микс языков',
        Constants.SCAND: 'Готик Аурорика',
        Constants.LATIN: 'Высокий Готик',
        Constants.SPAIN: 'Готик Иберика',
        Constants.ITALY: 'Готик Аппенин',
        Constants.POLAND: 'Готик Полоника',
        Constants.JAPAN: 'Готик Ниппон',
        Constants.ROMANIA: 'Готик Сильваника',
        Constants.HUNGARY: 'Готик Магьярика',
        Constants.TECH: 'Лингва Бинарика',
        Constants.CHINA: 'Готик Церес',
        Constants.GERMANY: 'Готик Тевтоника',
    },

    GENDER_KEY: {
        TYPE_KEY: 'строка',
        Constants.RANDOM: 'случайно выбранный пол',
        Constants.MALE: 'мужской',
        Constants.FEMALE: 'женский',
    },

    NOBILITY_KEY: {
        TYPE_KEY: 'строка',
        Constants.RANDOM: 'случайный выбор',
        Constants.NOBLE: 'генерировать благородное имя',
        Constants.SIMPLE: 'генерировать простое имя',
    },

    COUNT_KEY: {
        TYPE_KEY: 'целое число',
        'минимальное значение': 1,
        'максимальное значение': 50,
    }
}


@xframe_options_sameorigin
def main(request):
    return HttpResponseRedirect(reverse('index'))


@xframe_options_sameorigin
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
            response = render(request, 'namegen.html', {'form': form, 'names': names, 'version': version, })
            response['Access-Control-Allow-Origin'] = 'https://wiki.pandhammer.ru'
            return response
    else:
        form = NamegenForm()
        response = render(request, 'namegen.html', {'form': form, 'version': version, })
        response['Access-Control-Allow-Origin'] = 'https://wiki.pandhammer.ru'
        return response


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def get_name(request, format=None):
    err = '' + validate_request_data(request.data, NAMEGEN_APP_JSON_KEYS)
    lang = request.data.get(LANG_KEY, Constants.RANDOM)
    gender = request.data.get(GENDER_KEY, Constants.RANDOM)
    nobility = request.data.get(NOBILITY_KEY, Constants.RANDOM)
    count = request.data.get(COUNT_KEY, 1)
    if isinstance(count, str):
        if count.isdigit():
            count = int(count)
        else:
            if err != '':
                err += '; '
            err = 'количество имен должно быть целым числом'
            count = 1
    extra_errs = validate_data(lang, gender, nobility, count)
    if err != '':
        err += '; ' + extra_errs
    else:
        err = extra_errs
    if err != '':
        return Response({ERR_KEY: err}, status=status.HTTP_400_BAD_REQUEST)
    json = {'names': create_names(lang, gender, nobility, count)}
    return Response(json, status.HTTP_200_OK)


@api_view(['GET'])
def get_namegen_version(request, format=None):
    json = {APP_KEY: 'namegen', VERSION_KEY: version}
    return Response(json, status.HTTP_200_OK)


@api_view(['GET'])
def get_namegen_help(request, format=None):
    json = {APP_KEY: 'namegen',
            VERSION_KEY: version,
            API_ROOT_KEY: 'api/namegen/',
            API_KEY: {
                'ver': {
                    DESCRIPTION_KEY: 'узнать версию приложения',
                    METHOD_KEY: 'GET',
                    RETURN_KEY: 'строка, содержащая актуальную версию приложения'
                },
                'get': {
                    DESCRIPTION_KEY: 'сгенерировать одно или несколько имен персонажей',
                    METHOD_KEY: {
                        'POST': {
                            REQ_JSON_KEY: 'отсутствуют',
                            ALLOWED_JSON_KEY: {
                                'описание полей': {
                                    LANG_KEY: 'идентификатор языка, на основе которого генерируется имя (по '
                                              'умолчанию: R)',
                                    GENDER_KEY: 'идентификатор пола персонажа, для которого генерируется имя (по '
                                                'умолчанию: R)',
                                    NOBILITY_KEY: 'идентификатор, определяющий простое или благородное имя будет '
                                                  'сгенерировано (по умолчанию: R)',
                                    COUNT_KEY: 'количество имен, которое необходимо сгенерировать (по умолчанию: 1)',
                                },
                                'значения полей': FIELD_VALUES,
                            },
                            RETURN_KEY: 'массив сгенерированных имен',
                        },
                        'GET': {
                            DESCRIPTION_KEY: 'упрощенная версия. Эквивалентна POST-версии со значениями параметров по '
                                             'умолчанию.',
                            RETURN_KEY: 'строка, содержащее одно сгенерированное имя',
                        },
                    },
                },
                'help': {
                    DESCRIPTION_KEY: 'вызвать справку по API данного приложения',
                    METHOD_KEY: 'GET',
                    RETURN_KEY: 'JSON c информацией по API (скорее всего, вы уже вызвали данный метод, если это '
                                'читаете)'
                },
            }
            }
    return Response(json, status.HTTP_200_OK)


def validate_data(lang, gender, nobility, count):
    error = ''
    if lang.uppercase() not in LANG_IDS and lang.uppercase() != Constants.TECH \
            and lang.uppercase() != Constants.RANDOM:
        error += 'неизвестный ID языка'
    if gender.uppercase() != Constants.RANDOM and gender.uppercase() != Constants.MALE \
            and gender.uppercase() != Constants.FEMALE:
        if error != '':
            error += '; '
        error += 'неизвестный ID пола'
    if nobility.uppercase() != Constants.RANDOM and nobility.uppercase() != Constants.NOBLE \
            and nobility.uppercase() != Constants.SIMPLE:
        if error != '':
            error += '; '
        error += 'неизвестный ID благородства'
    if count < 1 or count > 50:
        if error != '':
            error += '; '
        error += 'количество имен за пределами разрешенного диапазона'
    return error


def validate_request_data(data, allowed_keys):
    err = ''
    for k in data.keys():
        if k not in allowed_keys:
            if err != '':
                err += '; '
            err += 'неподдерживаемое поле JSON: ' + k
    return err
