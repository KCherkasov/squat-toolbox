# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .methods import *

version = '1.12.0'

CONSONANTS = 'бвгджзйклмнпрстфхшщчц'
RIGHT_CONSONANTS = 'йнрс'
VOWELS = 'аеёиоуыэюя'


SLAVIC_CONNECTORS = {u'бр': u'а',   u'бм': u'и',    u'вл': u'ио',  u'вн': u'аия',   u'вс': u'уы',
                     u'вр': u'е',   u'вк': u'и',    u'вг': u'и',   u'гж': u'о',     u'гн': u'и',
                     u'гт': u'и',   u'гл': u'е',    u'дн': u'и',   u'дс': u'ио',    u'др': u'ие',
                     u'дв': u'оие', u'дц': u'и',    u'дж': u'е',   u'дм': u'о',     u'тф': u'а',
                     u'жн': u'еи',  u'жт': u'а',    u'жс': u'еи',  u'жш': u'и',     u'мг': u'аеи',
                     u'жк': u'и',   u'жг': u'и',    u'жл': u'аи',  u'зс': u'и',     u'зр': u'и',
                     u'зл': u'ое',  u'зт': u'и',    u'зщ': u'еи',  u'кж': u'и',     u'лш': u'ие',
                     u'лн': u'и',   u'лт': u'а',    u'лм': u'и',   u'лз': u'и',     u'лс': u'ио',
                     u'лп': u'и',   u'лв': u'оуиа', u'мн': u'и',   u'мз': u'и',     u'нш': u'ие',
                     u'нт': u'и',   u'нс': u'аи',   u'нр': u'а',   u'нм': u'и',     u'нл': u'и',
                     u'нж': u'ие',  u'нв': u'о',    u'пл': u'о',   u'рс': u'и',     u'рн': u'оие',
                     u'рф': u'о',   u'рт': u'ио',   u'рд': u'иу',  u'рм': u'и',     u'рц': u'оуи',
                     u'рл': u'оеу', u'рг': u'о',    u'сн': u'и',   u'ср': u'ие',    u'фн': u'еи',
                     u'сб': u'и',   u'см': u'и',    u'сл': u'е',   u'тн': u'и',     u'тр': u'о',
                     u'тл': u'ао',  u'тс': u'ауы',  u'тц': u'иы',  u'тм': u'и',     u'тб': u'и',
                     u'фз': u'и',   u'фс': u'и',    u'хн': u'о',   u'цн': u'ие',    u'цс': u'ие',
                     u'цр': u'е',   u'цб': u'и',    u'цш': u'еи',  u'цх': u'е',     u'цт': u'и',
                     u'цд': u'и',   u'цл': u'иеа',  u'чс': u'е',   u'чн': u'ие',    u'шл': u'уе',
                     u'рв': u'оуа', u'нф': u'и',    u'шв': u'оеа', u'жх': u'и',     u'тг': u'ои',
                     u'дл': u'иу',  u'чб': u'оие',  u'рж': u'иуы', u'хв': u'о',     u'зп': u'и',
                     u'вд': u'ие',  u'зм': u'ие',   u'сш': u'иеу', u'жф': u'и',     u'гф': u'оу',
                     u'нп': u'уио', u'кд': u'аио',  u'зд': u'и',   u'шм': u'и',     u'тш': u'и',
                     u'бк': u'еаи', u'шн': u'и',    u'гк': u'и',   u'кн': u'ие',    u'жв': u'и',
                     u'зн': u'иа',  u'кш': u'иеау', u'бс': u'иео', u'нд': u'ие',    u'бд': u'ои',
                     u'цг': u'еи',  u'гп': u'оуеи', u'лр': u'уои', u'чт': u'еи',    u'гш': u'ие',
                     u'гс': u'уо',  u'шч': u'иеу',  u'дт': u'оуи', u'бв': u'оаиуе', u'рх': u'аио',
                     u'рш': u'ио',  u'ст': u'и',    u'кв': u'оу',  u'мд': u'ие',    u'бт': u'иое',
                     u'мр': u'уои', u'вц': u'ие',   u'зк': u'ие',  u'шг': u'уиео',  u'мц': u'ие',
                     u'мф': u'еи',  u'вш': u'ие',   u'пс': u'ио',  u'сз': u'иаое',  u'рп': u'иеоу',
                     u'тв': u'иео', u'цм': u'иеа',  u'жщ': u'еи',  u'шд': u'оие',   u'кл': u'ау',
                     u'хл': u'ау',  u'тк': u'еои',  u'пг': u'оеи', u'кя': u'и',     u'гз': u'о',
                     u'жц': u'ие',  u'вм': u'и',    u'нц': u'ие',  u'цк': u'ие',    u'чж': u'ие',
                     u'жм': u'ие',  u'гч': u'оие',  u'жр': u'иое', u'нг': u'и',     u'дг': u'ои',
                     u'цз': u'иы',  u'нз': u'иеа',  u'лб': u'иа',  u'сж': u'иеа',   u'фд': u'и',
                     u'рщ': u'иеа', u'нк': u'и',    u'лг': u'и',   u'пж': u'иеа',   u'рз': u'и',
                     u'тз': u'ы',   u'цв': u'и',    u'гв': u'ие',  u'хс': u'а',     u'кс': u'а',
                     u'фт': u'а',   u'жз': u'еи',   u'дш': u'ие',  u'вж': u'ие',    u'фш': u'иеау',
                     u'бз': u'иеы', u'св': u'ао',   u'пр': u'аое', u'пм': u'иау',   u'дп': u'ие',
                     u'пц': u'еи',  u'чш': u'ие',   u'шз': u'уои', u'нх': u'ие',    u'лд': u'еиу',
                     u'сг': u'оие', u'чп': u'ие',   u'зц': u'ие',  u'тч': u'ыи',    u'чц': u'ие',
                     u'дщ': u'ы',   u'сщ': u'ы',    u'тщ': u'оы',  u'дк': u'е',     u'кц': u'аеи',
                     u'цф': u'ие',  u'гд': u'ои',   u'кг': u'оие', u'чд': u'иеа',   u'шр': u'уоие',
                     u'бл': u'еу',  u'хг': u'ои',   u'ск': u'ие',  u'тд': u'оуе',   u'вч': u'иеаоуы',
                     u'хт': u'е',   u'шт': u'е',    u'чм': u'ие',  u'хд': u'аио',   u'нщ': u'иеаы',
                     u'бц': u'еи',  u'вз': u'и',    u'мк': u'ие',  u'мв': u'о',     u'цч': u'аыеи',
                     u'ря': u'ьи',  u'чв': u'ео',   u'чл': u'е',   u'шц': u'иеы',   u'пя': u'и',
                     u'мс': u'ыио', u'гя': u'ьеи',  u'ця': u'ьеи', u'вя': u'ьие',   u'ня': u'ьие',
                     u'пд': u'иао', u'пт': u'иоа',  u'пв': u'ои',  u'пк': u'оа',    u'пн': u'иаео', }


ROMANIAN_CONNECTORS = {u'сн': u'а',      u'лн': u'иёае',  u'ра': u'ие',    u'ин': u'ае',   u'рд': u'иое',
                       u'йл': u'ое',     u'йр': u'о',     u'сд': u'иое',   u'ал': u'ияуо', u'нс': u'ие',
                       u'нд': u'иеэ',    u'нр': u'иео',   u'рк': u'ие',    u'йк': u'ио',   u'рл': u'иеоа',
                       u'сл': u'ие',     u'жл': u'еиу',   u'рн': u'ие',    u'нл': u'иаеу', u'зб': u'а',
                       u'сб': u'а',      u'зл': u'иеа',   u'тр': u'иеао',  u'рт': u'иео',  u'мт': u'иеа',
                       u'рц': u'уие',    u'мд': u'иу',    u'кн': u'уаеи',  u'лз': u'иае',  u'мц': u'иеа',
                       u'нц': u'иеу',    u'дз': u'иеа',   u'дс': u'иеа',   u'кл': u'аеэ',  u'хл': u'аеэ',
                       u'дб': u'иеа',    u'рс': u'ие',    u'дй': u'еоа',   u'лб': u'ие',   u'кр': u'иуа',
                       u'бр': u'е',      u'др': u'еи',    u'ср': u'еиа',   u'кс': u'иеа',  u'ст': u'иае',
                       u'фт': u'иае',    u'тф': u'еи',    u'бф': u'еи',    u'фб': u'еиа',  u'кф': u'иае',
                       u'фк': u'и',      u'фр': u'иа',    u'рф': u'ие',    u'цф': u'ие',   u'фц': u'еаи',
                       u'цр': u'еи',     u'цк': u'и',     u'кц': u'и',     u'цл': u'еаи',  u'лц': u'ие',
                       u'нт': u'иеа',    u'тн': u'иеа',   u'бн': u'ие',    u'нб': u'ие',   u'вл': u'иае',
                       u'лв': u'и',      u'кв': u'и',     u'вк': u'и',     u'фл': u'иеа',  u'лф': u'и',
                       u'цд': u'ие',     u'дц': u'и',     u'сц': u'еиа',   u'цс': u'и',    u'ле': u'и',
                       u'рз': u'и',      u'зр': u'ие',    u'гл': u'уеи',   u'лг': u'еаи',  u'рб': u'еаи',
                       u'зн': u'е',      u'нз': u'иеа',   u'лр': u'ие',    u'дм': u'ие',   u'тб': u'иеа',
                       u'бт': u'е',      u'кб': u'и',     u'бк': u'е',     u'зд': u'ие',   u'зс': u'ие',
                       u'сз': u'иеа',    u'нв': u'еи',    u'вн': u'ие',    u'бд': u'ие',   u'гс': u'ие',
                       u'сг': u'ие',     u'гц': u'ие',    u'цг': u'еи',    u'вг': u'ие',   u'гв': u'иаеоу',
                       u'лж': u'еи',     u'йц': u'ие',    u'цй': u'ие',    u'йг': u'еи',   u'гй': u'ие',
                       u'тс': u'иеу',    u'тл': u'иеаоу', u'лт': u'иеа',   u'гт': u'ие',   u'тг': u'ие',
                       u'вт': u'ие',     u'тв': u'ие',    u'вц': u'ие',    u'цв': u'и',    u'пц': u'и',
                       u'цп': u'и',      u'пв': u'ие',    u'вп': u'ие',    u'тп': u'и',    u'пт': u'ие',
                       u'фп': u'и',      u'пф': u'и',     u'кп': u'и',     u'пк': u'и',    u'мл': u'ие',
                       u'лм': u'иае',    u'гр': u'е',     u'рг': u'иеа',   u'дн': u'и',    u'жн': u'еи',
                       u'тм': u'иео',    u'лд': u'иеа',   u'рв': u'иеаэ',  u'тд': u'иеоа', u'дт': u'иео',
                       u'жд': u'аоеи',   u'нм': u'иеэа',  u'мн': u'иеаэ',  u'гд': u'уоиа', u'дг': u'уоиа',
                       u'дл': u'иеэа',   u'мб': u'ие',    u'бм': u'еи',    u'жр': u'иеа',  u'рж': u'еи',
                       u'тз': u'иеаэ',   u'зт': u'иеа',   u'кг': u'ие',    u'гк': u'ие',   u'кя': u'ие',
                       u'тя': u'ие',     u'ця': u'ие',    u'гя': u'ие',    u'жя': u'ие',   u'ря': u'ие',
                       u'дя': u'ие',     u'вя': u'ие',    u'ля': u'ие',    u'бя': u'ие',   u'фя': u'ие',
                       u'ся': u'ие',     u'зя': u'ие',    u'гм': u'иэеу',  u'сп': u'и',    u'пс': u'и',
                       u'жч': u'и',      u'чж': u'еау',   u'мр': u'иеу',   u'рм': u'иеу',  u'гн': u'эиеа',
                       u'нг': u'иеаэ',   u'вс': u'иеао',  u'св': u'иеао',  u'сч': u'иеа',  u'чс': u'иеа',
                       u'ьн': u'яаеи',   u'вз': u'иеэ',   u'зв': u'иеэу',  u'ьп': u'и',    u'жм': u'еи',
                       u'мж': u'ие',     u'км': u'иеуоа', u'мк': u'иеэ',   u'вд': u'иео',  u'дв': u'ие',
                       u'вр': u'иеоаэу', u'нк': u'ие',    u'жт': u'иеэ',   u'мф': u'иеоэ', u'фм': u'иеоэу',
                       u'тж': u'ие',     u'бл': u'иеэуа', u'йн': u'еи',    u'см': u'ие',   u'мс': u'иеуа',
                       u'хд': u'и',      u'дх': u'еиэу',  u'кй': u'иеэ',   u'пй': u'иеэ',  u'бй': u'иеэ',
                       u'хй': u'иеэ',    u'рй': u'иеэ',   u'мй': u'иеэ',   u'нй': u'иеэ',  u'ьй': u'иеэ',
                       u'жй': u'ие',     u'вй': u'иеэ',   u'зй': u'иеэ',   u'лй': u'иеэ',  u'сй': u'иеэ',
                       u'тй': u'иеэ',    u'фй': u'иеэ',   u'нп': u'иеэоу', u'пн': u'иеоа', u'сж': u'ие',
                       u'жс': u'иеа',    u'дк': u'иеоэ',  u'кд': u'иеэау', u'гж': u'ие',   u'жг': u'ие',
                       u'зм': u'иеэ',    u'мз': u'эуеа',  u'сф': u'ие',    u'фс': u'оиеэ', u'кч': u'уоеиа',
                       u'мя': u'ие',     u'ня': u'ие',    u'гз': u'иеэо',  u'зг': u'иеэу', u'мп': u'и',
                       u'пм': u'аеэ',    u'гф': u'иеоу',  u'фг': u'иеа',   u'жк': u'еиэ',  u'кж': u'ие',
                       u'жф': u'ие',     u'фж': u'иеуо',  u'гп': u'ие',    u'бч': u'еи',   u'йб': u'оуаэ',
                       u'нч': u'эие',    u'рп': u'иэе',   u'лс': u'оиуэе', u'вф': u'иеэ',  u'фв': u'иеэ',
                       u'фн': u'эаиео',  u'хз': u'иеэ',   u'кз': u'иэе',
                       }


GERMAN_CONNECTORS = {u'дл': u'оаеиу', u'гн': u'ие',   u'лн': u'иоеа', u'лх': u'',    u'мл': u'аеи',
                     u'лк': u'и',     u'нл': u'уоае', u'нм': u'ае',   u'сл': u'иое', u'тл': u'аиео',
                     u'бл': u'аи',    u'бр': u'ае',   u'нд': u'ие',   u'жт': u'и',   u'нх': u'ие',
                     u'нг': u'ие',    u'рн': u'еи',   u'бк': u'ие',   u'гб': u'е',   u'лд': u'ие',
                     u'нв': u'о',     u'тт': u'',     u'сф': u'еи',   u'зф': u'еи',  u'рк': u'и',
                     u'вн': u'о',     u'вт': u'е',    u'зл': u'оае',  u'лс': u'ие',  u'мк': u'ие',
                     u'жб': u'е',     u'кл': u'ие',   u'лй': u'ае',   u'лт': u'оие', u'тр': u'аеио',
                     u'тн': u'иеа',   u'рс': u'ие',   u'рм': u'иа',   u'дй': u'а',   u'дн': u'и',
                     u'зн': u'е',     u'сн': u'е',    u'нб': u'ие',   u'сб': u'аеи', u'зб': u'аеи',
                     u'гр': u'ае',    u'рй': u'е',    u'рл': u'ие',   u'св': u'ие',  u'хс': u'е',
                     u'пр': u'е',     u'пн': u'ие',   u'пб': u'аи',   u'пв': u'ие',  u'пл': u'о',
                     u'ня': u'иь',    u'мя': u'иь',   u'ля': u'ьи',   u'бя': u'ьи',  u'гя': u'ьи',
                     u'вя': u'ьи',    u'дя': u'иь',   u'жя': u'иь',   u'зя': u'ьи',  u'ся': u'ьи',
                     u'кя': u'ьи',    u'пя': u'ья',   u'ря': u'ья',   u'фя': u'ьи',  u'хя': u'ьи',
                     u'шя': u'ьи',    u'чя': u'ьи',   u'мр': u'аие',  u'тя': u'ьи',  u'рз': u'е',
                     u'лц': u'и',     u'бц': u'и',    u'вц': u'и',    u'гц': u'и',   u'дц': u'и',
                     u'жц': u'ие',    u'зц': u'и',    u'кц': u'и',    u'мц': u'ие',  u'нц': u'и',
                     u'пц': u'ие',    u'рц': u'ие',   u'сц': u'ие',   u'фц': u'ие',  u'хц': u'и',
                     u'шц': u'и',     u'дг': u'ие',   u'лр': u'ая',   u'гс': u'уаи', u'лб': u'ь',
                     u'лв': u'ь',     u'др': u'ае',   u'лл': u'оау',  u'дф': u'оау', u'гф': u'оау',
                     u'лм': u'ь',     u'дм': u'е',    u'гм': u'е',    u'дс': u'и',   u'мс': u'и',
                     u'гз': u'и',     u'лз': u'и',    u'мз': u'и',    u'вз': u'и',   u'дз': u'и',
                     u'фс': u'еи',    u'фз': u'ие',   u'фр': u'иеа',  u'фм': u'иае', u'фв': u'еи',
                     u'фл': u'уоаи',  u'фх': u'и',    u'ьл': u'уоаи', u'нк': u'ие',  u'дк': u'и',
                     u'хл': u'оуаи',  u'тс': u'и',    u'тг': u'ие',   u'нф': u'и',   u'бс': u'а',
                     u'цф': u'и',     u'цв': u'и',    u'цл': u'оуиа', u'лп': u'и',   u'рп': u'и',
                     u'бп': u'и',     u'вп': u'и',    u'гп': u'и',    u'дп': u'и',   u'жп': u'и',
                     u'зп': u'и',     u'мп': u'и',    u'ьп': u'и',    u'нп': u'и',   u'сп': u'и',
                     u'тп': u'и',     u'фп': u'и',    u'хп': u'и',    u'шп': u'и',   u'чп': u'и',
                     u'жн': u'ие',    u'жг': u'ие',   u'жв': u'ие',   u'жд': u'ие',  u'жз': u'ие',
                     u'жк': u'ие',    u'жл': u'ие',   u'жм': u'ие',   u'жр': u'ие',  u'жс': u'ие',
                     u'жф': u'ие',    u'жх': u'ие',   u'жч': u'ие',   u'кр': u'е',   u'цн': u'ие',
                     u'фн': u'иеоа',
                     }


GERMAN_BLANK_CONNECTORS = [u'мм', u'рм', u'нт', u'рт', u'лф', u'лл', u'нх', u'нг', u'рн', u'лв',
                           u'лм', u'нр', u'лб', u'гл', u'см', u'зм', u'нн', u'гр', u'зб', u'сб',
                           u'тр', u'мг', u'мх', u'рм', u'нз', u'нс', u'бр', u'лм', u'гб', u'гн',
                           u'лх', u'лб', u'лв', u'др', u'гм', u'фх', u'фв', u'нк', u'нх', u'нг',
                           u'н',  u'тг', u'св', u'', u'', u'', u'', u'', u'', ]


HUNGARIAN_CONNECTORS = {}


HUNGARIAN_BLANK_CONNECTORS = [u'ра', u'лз', u'нд', u'тр', u'кс',
                              u'ле', u'нк', u'нз', u'ин', u'пк', u'кч', u'', u'', ]


ROMANIAN_BLANK_CONNECTORS = [u'ра', u'лз', u'нд', u'тр', u'кс', u'', u'',
                             u'ле', u'нк', u'нз', u'ин', u'пк', u'дм', u'кч', u'нч', ]


SLAVIC_BLANK_CONNECTORS = [u'бр', u'вд', u'дм', u'дв', u'жб', u'зб', u'сб', u'зв', u'йц', u'лр', u'лж',
                           u'нг', u'нк', u'нт', u'нц', u'рг', u'рк', u'рж', u'рц', u'шк', u'рв',
                           u'лв', u'шм', u'рц', u'рш', u'зм', u'кл', u'цк', u'дв', ]

GENETOR = u'Генетор'
CYBERNETICA = u'Легио Кибернетика'
REDUCTOR = u'Ордо Редуктор'
TITANICA = u'Коллегия Титаника'
MYRMIDON = u'Ауксилия Мирмидон'
MAGI = u'Механикум'
LOGI = u'Логис'
ARTISAN = u'Артизан'

LANGS = NamegenForm.LANGS
LANG_IDS = [Constants.SCAND, Constants.LATIN, Constants.SPAIN, Constants.ITALY, Constants.POLAND, Constants.JAPAN,
            Constants.ROMANIA, Constants.HUNGARY, Constants.CHINA, Constants.GERMANY]


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
            names = list()
            if lang == Constants.SCAND:
                first_parts_male = MaleScand.objects.get_first_parts_list()
                second_parts_male = MaleScand.objects.get_second_parts_list()

                first_parts_female = FemaleScand.objects.get_first_parts_list()
                second_parts_female = FemaleScand.objects.get_second_parts_list()

                if count == 1:
                    names.append(generate_name_scand(gender, nobility, first_parts_male, second_parts_male,
                                                     first_parts_female, second_parts_female))
                else:
                    names = generate_names_scand(gender, nobility, first_parts_male, second_parts_male,
                                                 first_parts_female, second_parts_female, count)
            elif lang == Constants.LATIN:
                first_parts_male = MaleLatin.objects.get_first_parts_list()
                second_parts_male = MaleLatin.objects.get_second_parts_list()

                first_parts_female = FemaleLatin.objects.get_first_parts_list()
                second_parts_female = FemaleLatin.objects.get_second_parts_list()

                cognomen_first_parts = CognomenLatin.objects.get_first_parts_list()
                cognomen_second_parts_male = CognomenLatin.objects.get_second_parts_male_list()
                cognomen_second_parts_female = CognomenLatin.objects.get_second_parts_female_list()

                if count == 1:
                    names.append(generate_name_latin(gender, nobility,
                                                     first_parts_male, second_parts_male,
                                                     first_parts_female, second_parts_female,
                                                     cognomen_first_parts, cognomen_second_parts_male,
                                                     cognomen_second_parts_female))
                else:
                    names = generate_names_latin(gender, nobility, count,
                                                 first_parts_male, second_parts_male,
                                                 first_parts_female, second_parts_female,
                                                 cognomen_first_parts, cognomen_second_parts_male,
                                                 cognomen_second_parts_female)
            elif lang == Constants.SPAIN:
                first_parts_male = MaleSpanish.objects.get_first_parts_list()
                second_parts_male = MaleSpanish.objects.get_second_parts_list()

                first_parts_female = FemaleSpanish.objects.get_first_parts_list()
                second_parts_female = FemaleSpanish.objects.get_second_parts_list()

                if count == 1:
                    names.append(generate_name_spanish(gender, nobility,
                                                       first_parts_male, second_parts_male,
                                                       first_parts_female, second_parts_female))
                else:
                    names = generate_names_spanish(gender, nobility, count,
                                                   first_parts_male, second_parts_male,
                                                   first_parts_female, second_parts_female)
            elif lang == Constants.ITALY:
                first_parts_male = MaleItalian.objects.get_first_parts_list()
                second_parts_male = MaleItalian.objects.get_second_parts_list()

                first_parts_female = FemaleItalian.objects.get_first_parts_list()
                second_parts_female = FemaleItalian.objects.get_second_parts_list()

                surnames_first_part = SurnamesItalian.objects.get_first_parts_list()
                surnames_second_part = SurnamesItalian.objects.get_second_parts_list()

                if count == 1:
                    names.append(generate_name_italian(gender, nobility,
                                                       first_parts_male, second_parts_male,
                                                       first_parts_female, second_parts_female,
                                                       surnames_first_part, surnames_second_part))
                else:
                    names = generate_names_italian(gender, nobility, count,
                                                   first_parts_male, second_parts_male,
                                                   first_parts_female, second_parts_female,
                                                   surnames_first_part, surnames_second_part)
            elif lang == Constants.POLAND:
                first_parts_male = MalePolish.objects.get_first_parts_list()
                second_parts_male = MalePolish.objects.get_second_parts_list()

                first_parts_female = FemalePolish.objects.get_first_parts_list()
                second_parts_female = FemalePolish.objects.get_second_parts_list()

                surname_firsts = SurnamesPolish.objects.get_first_parts_list()
                surname_seconds = SurnamesPolish.objects.get_second_parts_list()

                surname_ends_male = SurnamesPolishEnd.objects.get_male_endings()
                surname_ends_female = SurnamesPolishEnd.objects.get_female_endings()
                if count == 1:
                    names.append(generate_name_polish(gender, nobility,
                                                      first_parts_male, second_parts_male,
                                                      first_parts_female, second_parts_female,
                                                      surname_firsts, surname_seconds,
                                                      surname_ends_male, surname_ends_female))
                else:
                    names = generate_names_polish(gender, nobility, count,
                                                  first_parts_male, second_parts_male,
                                                  first_parts_female, second_parts_female,
                                                  surname_firsts, surname_seconds,
                                                  surname_ends_male, surname_ends_female)
            elif lang == Constants.JAPAN:
                first_parts_male = MaleJapanese.objects.get_first_parts_list()
                second_parts_male = MaleJapanese.objects.get_second_parts_list()

                first_parts_female = FemaleJapanese.objects.get_first_parts_list()
                second_parts_female = FemaleJapanese.objects.get_second_parts_list()

                surname_firsts = SurnamesJapanese.objects.get_first_parts_list()
                surname_seconds = SurnamesJapanese.objects.get_second_parts_list()

                if count == 1:
                    names.append(generate_name_japanese(gender, nobility,
                                                        first_parts_male, second_parts_male,
                                                        first_parts_female, second_parts_female,
                                                        surname_firsts, surname_seconds))
                else:
                    names = generate_names_japanese(gender, nobility, count,
                                                    first_parts_male, second_parts_male,
                                                    first_parts_female, second_parts_female,
                                                    surname_firsts, surname_seconds)
            elif lang == Constants.TECH:
                [first_parts_male, second_parts_male, first_parts_female, second_parts_female,
                 cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
                 surname_italian_firsts, surname_italian_seconds,
                 surname_polish_firsts, surname_polish_seconds,
                 surname_polish_ends_male, surname_polish_ends_female,
                 surname_japanese_firsts, surname_japanese_seconds,
                 surname_romanian_firsts, surname_romanian_seconds,
                 surname_chinese_firsts, surname_chinese_seconds,
                 surname_german_firsts, surname_german_seconds] = prepare_data_rand_namegen()

                [ranks_simple, ranks_noble_magi, ranks_noble_genetor,
                 ranks_noble_logi, ranks_noble_artisan, ranks_noble_myrmidon,
                 cults, letters, text_numbers] = prepare_lists_techno()

                if count == 1:
                    names.append(generate_name_techno(gender, nobility, letters, text_numbers, cults,
                                                      ranks_simple, ranks_noble_magi, ranks_noble_genetor,
                                                      ranks_noble_logi, ranks_noble_artisan, ranks_noble_myrmidon,
                                                      first_parts_male, second_parts_male, first_parts_female,
                                                      second_parts_female, cognomen_firsts, cognomen_seconds_male,
                                                      cognomen_seconds_female, surname_italian_firsts,
                                                      surname_italian_seconds, surname_polish_firsts,
                                                      surname_polish_seconds, surname_polish_ends_male,
                                                      surname_polish_ends_female, surname_japanese_firsts,
                                                      surname_japanese_seconds))
                else:
                    names = generate_names_techno(gender, nobility, count, letters, text_numbers, cults,
                                                  ranks_simple, ranks_noble_magi, ranks_noble_genetor,
                                                  ranks_noble_logi, ranks_noble_artisan, ranks_noble_myrmidon,
                                                  first_parts_male, second_parts_male, first_parts_female,
                                                  second_parts_female, cognomen_firsts, cognomen_seconds_male,
                                                  cognomen_seconds_female, surname_italian_firsts,
                                                  surname_italian_seconds, surname_polish_firsts,
                                                  surname_polish_seconds, surname_polish_ends_male,
                                                  surname_polish_ends_female, surname_japanese_firsts,
                                                  surname_japanese_seconds)
            elif lang == Constants.ROMANIA:
                first_parts_male = MaleRomanian.objects.get_first_parts_list()
                second_parts_male = MaleRomanian.objects.get_second_parts_list()

                first_parts_female = FemaleRomanian.objects.get_first_parts_list()
                second_parts_female = FemaleRomanian.objects.get_second_parts_list()

                surname_firsts = SurnamesRomanian.objects.get_firsts_list()
                surname_seconds = SurnamesRomanian.objects.get_seconds_list()

                cognomen_firsts = CognomenLatin.objects.get_first_parts_list()
                cognomen_seconds_male = CognomenLatin.objects.get_second_parts_male_list()
                cognomen_seconds_female = CognomenLatin.objects.get_second_parts_male_list()

                if count == 1:
                    names.append(generate_name_romanian(gender, nobility,
                                                        first_parts_male, second_parts_male,
                                                        first_parts_female, second_parts_female,
                                                        surname_firsts, surname_seconds, cognomen_firsts,
                                                        cognomen_seconds_male, cognomen_seconds_female))
                else:
                    names = generate_names_romanian(gender, nobility, count,
                                                    first_parts_male, second_parts_male,
                                                    first_parts_female, second_parts_female,
                                                    surname_firsts, surname_seconds, cognomen_firsts,
                                                    cognomen_seconds_male, cognomen_seconds_female)
            elif lang == Constants.HUNGARY:
                first_parts_male = MaleHungarian.objects.get_first_parts_list()
                second_parts_male = MaleHungarian.objects.get_second_parts_list()

                first_parts_female = FemaleHungarian.objects.get_first_parts_list()
                second_parts_female = FemaleHungarian.objects.get_second_parts_list()

                surname_firsts = SurnamesRomanian.objects.get_firsts_list()
                surname_seconds = SurnamesRomanian.objects.get_seconds_list()

                cognomen_firsts = CognomenLatin.objects.get_first_parts_list()
                cognomen_seconds_male = CognomenLatin.objects.get_second_parts_male_list()
                cognomen_seconds_female = CognomenLatin.objects.get_second_parts_male_list()

                if count == 1:
                    names.append(generate_name_hungarian(gender, nobility,
                                                         first_parts_male, second_parts_male,
                                                         first_parts_female, second_parts_female,
                                                         surname_firsts, surname_seconds, cognomen_firsts,
                                                         cognomen_seconds_male, cognomen_seconds_female))
                else:
                    names = generate_names_hungarian(gender, nobility, count,
                                                     first_parts_male, second_parts_male,
                                                     first_parts_female, second_parts_female,
                                                     surname_firsts, surname_seconds, cognomen_firsts,
                                                     cognomen_seconds_male, cognomen_seconds_female)
            elif lang == Constants.CHINA:
                first_parts_male = MaleChinese.objects.get_first_parts_list()
                second_parts_male = MaleChinese.objects.get_second_parts_list()

                first_parts_female = FemaleChinese.objects.get_first_parts_list()
                second_parts_female = FemaleChinese.objects.get_second_parts_list()

                surname_firsts = SurnamesChinese.objects.get_first_parts_list()
                surname_seconds = SurnamesChinese.objects.get_second_parts_list()

                if count == 1:
                    names.append(generate_name_chinese(gender, nobility,
                                                       first_parts_male, second_parts_male,
                                                       first_parts_female, second_parts_female,
                                                       surname_firsts, surname_seconds))
                else:
                    names = generate_names_chinese(gender, nobility, count,
                                                   first_parts_male, second_parts_male,
                                                   first_parts_female, second_parts_female,
                                                   surname_firsts, surname_seconds)
            elif lang == Constants.GERMANY:
                first_parts_male = MaleGerman.objects.get_first_parts_list()
                second_parts_male = MaleGerman.objects.get_second_parts_list()

                first_parts_female = FemaleGerman.objects.get_first_parts_list()
                second_parts_female = FemaleGerman.objects.get_second_parts_list()

                surname_firsts = SurnamesGerman.objects.get_first_parts_list()
                surname_seconds = SurnamesGerman.objects.get_second_parts_list()

                if count == 1:
                    names.append(generate_name_german(gender, nobility,
                                                      first_parts_male, second_parts_male,
                                                      first_parts_female, second_parts_female,
                                                      surname_firsts, surname_seconds))
                else:
                    names = generate_names_german(gender, nobility, count,
                                                  first_parts_male, second_parts_male,
                                                  first_parts_female, second_parts_female,
                                                  surname_firsts, surname_seconds)
            elif lang == Constants.RANDOM:
                [first_parts_male, second_parts_male, first_parts_female, second_parts_female,
                 cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
                 surname_italian_firsts, surname_italian_seconds,
                 surname_polish_firsts, surname_polish_seconds,
                 surname_polish_ends_male, surname_polish_ends_female,
                 surname_japanese_firsts, surname_japanese_seconds,
                 surname_romanian_firsts, surname_romanian_seconds,
                 surname_chinese_firsts, surname_chinese_seconds,
                 surname_german_firsts, surname_german_seconds] = prepare_data_rand_namegen()
                if count == 1:
                    names.append(generate_name_rand(gender, nobility,
                                                    first_parts_male, second_parts_male,
                                                    first_parts_female, second_parts_female,
                                                    cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
                                                    surname_italian_firsts, surname_italian_seconds,
                                                    surname_polish_firsts, surname_polish_seconds,
                                                    surname_polish_ends_male, surname_polish_ends_female,
                                                    surname_japanese_firsts, surname_japanese_seconds,
                                                    surname_romanian_firsts, surname_romanian_seconds,
                                                    surname_chinese_firsts, surname_chinese_seconds,
                                                    surname_german_firsts, surname_german_seconds))
                else:
                    names = generate_names_rand(gender, nobility, count,
                                                first_parts_male, second_parts_male,
                                                first_parts_female, second_parts_female,
                                                cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
                                                surname_italian_firsts, surname_italian_seconds,
                                                surname_polish_firsts, surname_polish_seconds,
                                                surname_polish_ends_male, surname_polish_ends_female,
                                                surname_japanese_firsts, surname_japanese_seconds,
                                                surname_romanian_firsts, surname_romanian_seconds,
                                                surname_chinese_firsts, surname_chinese_seconds,
                                                surname_german_firsts, surname_german_seconds)

            return render(request, 'namegen.html', {'form': form, 'names': names, 'version': version, })
    else:
        form = NamegenForm()

        return render(request, 'namegen.html', {'form': form, 'version': version, })


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


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def get_name(request, format=None):
    lang = request.data.get('lang', 'R')
    gender = request.data.get('gender', 'R')
    nobility = request.data.get('nobility', 'R')
    count = request.data.get('count', 1)

    err = ''
    if isinstance(count, str):
        if count.isdigit():
            count = int(count)
        else:
            err = 'names count must be an integer'
    extra_errs = validate_data(lang, gender, nobility, count)
    if err != '':
        err += '; ' + extra_errs
    else:
        err = extra_errs
    if err != '':
        return Response({'errors': err}, status=status.HTTP_400_BAD_REQUEST)
    names = list()
    if lang == Constants.SCAND:
        first_parts_male = MaleScand.objects.get_first_parts_list()
        second_parts_male = MaleScand.objects.get_second_parts_list()

        first_parts_female = FemaleScand.objects.get_first_parts_list()
        second_parts_female = FemaleScand.objects.get_second_parts_list()

        if count == 1:
            names.append(generate_name_scand(gender, nobility, first_parts_male, second_parts_male,
                                             first_parts_female, second_parts_female))
        else:
            names = generate_names_scand(gender, nobility, first_parts_male, second_parts_male,
                                         first_parts_female, second_parts_female, count)
    elif lang == Constants.LATIN:
        first_parts_male = MaleLatin.objects.get_first_parts_list()
        second_parts_male = MaleLatin.objects.get_second_parts_list()

        first_parts_female = FemaleLatin.objects.get_first_parts_list()
        second_parts_female = FemaleLatin.objects.get_second_parts_list()

        cognomen_first_parts = CognomenLatin.objects.get_first_parts_list()
        cognomen_second_parts_male = CognomenLatin.objects.get_second_parts_male_list()
        cognomen_second_parts_female = CognomenLatin.objects.get_second_parts_female_list()

        if count == 1:
            names.append(generate_name_latin(gender, nobility,
                                             first_parts_male, second_parts_male,
                                             first_parts_female, second_parts_female,
                                             cognomen_first_parts, cognomen_second_parts_male,
                                             cognomen_second_parts_female))
        else:
            names = generate_names_latin(gender, nobility, count,
                                         first_parts_male, second_parts_male,
                                         first_parts_female, second_parts_female,
                                         cognomen_first_parts, cognomen_second_parts_male,
                                         cognomen_second_parts_female)
    elif lang == Constants.SPAIN:
        first_parts_male = MaleSpanish.objects.get_first_parts_list()
        second_parts_male = MaleSpanish.objects.get_second_parts_list()

        first_parts_female = FemaleSpanish.objects.get_first_parts_list()
        second_parts_female = FemaleSpanish.objects.get_second_parts_list()

        if count == 1:
            names.append(generate_name_spanish(gender, nobility,
                                               first_parts_male, second_parts_male,
                                               first_parts_female, second_parts_female))
        else:
            names = generate_names_spanish(gender, nobility, count,
                                           first_parts_male, second_parts_male,
                                           first_parts_female, second_parts_female)
    elif lang == Constants.ITALY:
        first_parts_male = MaleItalian.objects.get_first_parts_list()
        second_parts_male = MaleItalian.objects.get_second_parts_list()

        first_parts_female = FemaleItalian.objects.get_first_parts_list()
        second_parts_female = FemaleItalian.objects.get_second_parts_list()

        surnames_first_part = SurnamesItalian.objects.get_first_parts_list()
        surnames_second_part = SurnamesItalian.objects.get_second_parts_list()

        if count == 1:
            names.append(generate_name_italian(gender, nobility,
                                               first_parts_male, second_parts_male,
                                               first_parts_female, second_parts_female,
                                               surnames_first_part, surnames_second_part))
        else:
            names = generate_names_italian(gender, nobility, count,
                                           first_parts_male, second_parts_male,
                                           first_parts_female, second_parts_female,
                                           surnames_first_part, surnames_second_part)
    elif lang == Constants.POLAND:
        first_parts_male = MalePolish.objects.get_first_parts_list()
        second_parts_male = MalePolish.objects.get_second_parts_list()

        first_parts_female = FemalePolish.objects.get_first_parts_list()
        second_parts_female = FemalePolish.objects.get_second_parts_list()

        surname_firsts = SurnamesPolish.objects.get_first_parts_list()
        surname_seconds = SurnamesPolish.objects.get_second_parts_list()

        surname_ends_male = SurnamesPolishEnd.objects.get_male_endings()
        surname_ends_female = SurnamesPolishEnd.objects.get_female_endings()
        if count == 1:
            names.append(generate_name_polish(gender, nobility,
                                              first_parts_male, second_parts_male,
                                              first_parts_female, second_parts_female,
                                              surname_firsts, surname_seconds,
                                              surname_ends_male, surname_ends_female))
        else:
            names = generate_names_polish(gender, nobility, count,
                                          first_parts_male, second_parts_male,
                                          first_parts_female, second_parts_female,
                                          surname_firsts, surname_seconds,
                                          surname_ends_male, surname_ends_female)

    elif lang == Constants.JAPAN:
        first_parts_male = MaleJapanese.objects.get_first_parts_list()
        second_parts_male = MaleJapanese.objects.get_second_parts_list()

        first_parts_female = FemaleJapanese.objects.get_first_parts_list()
        second_parts_female = FemaleJapanese.objects.get_second_parts_list()

        surname_firsts = SurnamesJapanese.objects.get_first_parts_list()
        surname_seconds = SurnamesJapanese.objects.get_second_parts_list()

        if count == 1:
            names.append(generate_name_japanese(gender, nobility,
                                                first_parts_male, second_parts_male,
                                                first_parts_female, second_parts_female,
                                                surname_firsts, surname_seconds))
        else:
            names = generate_names_japanese(gender, nobility, count,
                                            first_parts_male, second_parts_male,
                                            first_parts_female, second_parts_female,
                                            surname_firsts, surname_seconds)
    elif lang == Constants.TECH:
        [first_parts_male, second_parts_male, first_parts_female, second_parts_female,
         cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
         surname_italian_firsts, surname_italian_seconds,
         surname_polish_firsts, surname_polish_seconds,
         surname_polish_ends_male, surname_polish_ends_female,
         surname_japanese_firsts, surname_japanese_seconds,
         surname_romanian_firsts, surname_romanian_seconds,
         surname_chinese_firsts, surname_chinese_seconds,
         surname_german_firsts, surname_german_seconds] = prepare_data_rand_namegen()

        [ranks_simple, ranks_noble_magi, ranks_noble_genetor,
         ranks_noble_logi, ranks_noble_artisan, ranks_noble_myrmidon,
         cults, letters, text_numbers] = prepare_lists_techno()

        if count == 1:
            names.append(generate_name_techno(gender, nobility, letters, text_numbers, cults,
                                              ranks_simple, ranks_noble_magi, ranks_noble_genetor,
                                              ranks_noble_logi, ranks_noble_artisan, ranks_noble_myrmidon,
                                              first_parts_male, second_parts_male, first_parts_female,
                                              second_parts_female, cognomen_firsts, cognomen_seconds_male,
                                              cognomen_seconds_female, surname_italian_firsts,
                                              surname_italian_seconds, surname_polish_firsts,
                                              surname_polish_seconds, surname_polish_ends_male,
                                              surname_polish_ends_female, surname_japanese_firsts,
                                              surname_japanese_seconds))
        else:
            names = generate_names_techno(gender, nobility, count, letters, text_numbers, cults,
                                          ranks_simple, ranks_noble_magi, ranks_noble_genetor,
                                          ranks_noble_logi, ranks_noble_artisan, ranks_noble_myrmidon,
                                          first_parts_male, second_parts_male, first_parts_female,
                                          second_parts_female, cognomen_firsts, cognomen_seconds_male,
                                          cognomen_seconds_female, surname_italian_firsts,
                                          surname_italian_seconds, surname_polish_firsts,
                                          surname_polish_seconds, surname_polish_ends_male,
                                          surname_polish_ends_female, surname_japanese_firsts,
                                          surname_japanese_seconds)
    elif lang == Constants.ROMANIA:
        first_parts_male = MaleRomanian.objects.get_first_parts_list()
        second_parts_male = MaleRomanian.objects.get_second_parts_list()

        first_parts_female = FemaleRomanian.objects.get_first_parts_list()
        second_parts_female = FemaleRomanian.objects.get_second_parts_list()

        surname_firsts = SurnamesRomanian.objects.get_firsts_list()
        surname_seconds = SurnamesRomanian.objects.get_seconds_list()

        cognomen_firsts = CognomenLatin.objects.get_first_parts_list()
        cognomen_seconds_male = CognomenLatin.objects.get_second_parts_male_list()
        cognomen_seconds_female = CognomenLatin.objects.get_second_parts_male_list()

        if count == 1:
            names.append(generate_name_romanian(gender, nobility,
                                                first_parts_male, second_parts_male,
                                                first_parts_female, second_parts_female,
                                                surname_firsts, surname_seconds, cognomen_firsts,
                                                cognomen_seconds_male, cognomen_seconds_female))
        else:
            names = generate_names_romanian(gender, nobility, count,
                                            first_parts_male, second_parts_male,
                                            first_parts_female, second_parts_female,
                                            surname_firsts, surname_seconds, cognomen_firsts,
                                            cognomen_seconds_male, cognomen_seconds_female)
    elif lang == Constants.HUNGARY:
        first_parts_male = MaleHungarian.objects.get_first_parts_list()
        second_parts_male = MaleHungarian.objects.get_second_parts_list()

        first_parts_female = FemaleHungarian.objects.get_first_parts_list()
        second_parts_female = FemaleHungarian.objects.get_second_parts_list()

        surname_firsts = SurnamesRomanian.objects.get_firsts_list()
        surname_seconds = SurnamesRomanian.objects.get_seconds_list()

        cognomen_firsts = CognomenLatin.objects.get_first_parts_list()
        cognomen_seconds_male = CognomenLatin.objects.get_second_parts_male_list()
        cognomen_seconds_female = CognomenLatin.objects.get_second_parts_male_list()

        if count == 1:
            names.append(generate_name_hungarian(gender, nobility,
                                                 first_parts_male, second_parts_male,
                                                 first_parts_female, second_parts_female,
                                                 surname_firsts, surname_seconds, cognomen_firsts,
                                                 cognomen_seconds_male, cognomen_seconds_female))
        else:
            names = generate_names_hungarian(gender, nobility, count,
                                             first_parts_male, second_parts_male,
                                             first_parts_female, second_parts_female,
                                             surname_firsts, surname_seconds, cognomen_firsts,
                                             cognomen_seconds_male, cognomen_seconds_female)
    elif lang == Constants.CHINA:
        first_parts_male = MaleChinese.objects.get_first_parts_list()
        second_parts_male = MaleChinese.objects.get_second_parts_list()

        first_parts_female = FemaleChinese.objects.get_first_parts_list()
        second_parts_female = FemaleChinese.objects.get_second_parts_list()

        surname_firsts = SurnamesChinese.objects.get_first_parts_list()
        surname_seconds = SurnamesChinese.objects.get_second_parts_list()

        if count == 1:
            names.append(generate_name_chinese(gender, nobility,
                                               first_parts_male, second_parts_male,
                                               first_parts_female, second_parts_female,
                                               surname_firsts, surname_seconds))
        else:
            names = generate_names_chinese(gender, nobility, count,
                                           first_parts_male, second_parts_male,
                                           first_parts_female, second_parts_female,
                                           surname_firsts, surname_seconds)
    elif lang == Constants.GERMANY:
        first_parts_male = MaleGerman.objects.get_first_parts_list()
        second_parts_male = MaleGerman.objects.get_second_parts_list()

        first_parts_female = FemaleGerman.objects.get_first_parts_list()
        second_parts_female = FemaleGerman.objects.get_second_parts_list()

        surname_firsts = SurnamesGerman.objects.get_first_parts_list()
        surname_seconds = SurnamesGerman.objects.get_second_parts_list()

        if count == 1:
            names.append(generate_name_german(gender, nobility,
                                              first_parts_male, second_parts_male,
                                              first_parts_female, second_parts_female,
                                              surname_firsts, surname_seconds))
        else:
            names = generate_names_german(gender, nobility, count,
                                          first_parts_male, second_parts_male,
                                          first_parts_female, second_parts_female,
                                          surname_firsts, surname_seconds)
    elif lang == Constants.RANDOM:
        [first_parts_male, second_parts_male, first_parts_female, second_parts_female,
         cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
         surname_italian_firsts, surname_italian_seconds,
         surname_polish_firsts, surname_polish_seconds,
         surname_polish_ends_male, surname_polish_ends_female,
         surname_japanese_firsts, surname_japanese_seconds,
         surname_romanian_firsts, surname_romanian_seconds,
         surname_chinese_firsts, surname_chinese_seconds,
         surname_german_firsts, surname_german_seconds] = prepare_data_rand_namegen()
        if count == 1:
            names.append(generate_name_rand(gender, nobility,
                                            first_parts_male, second_parts_male,
                                            first_parts_female, second_parts_female,
                                            cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
                                            surname_italian_firsts, surname_italian_seconds,
                                            surname_polish_firsts, surname_polish_seconds,
                                            surname_polish_ends_male, surname_polish_ends_female,
                                            surname_japanese_firsts, surname_japanese_seconds,
                                            surname_romanian_firsts, surname_romanian_seconds,
                                            surname_chinese_firsts, surname_chinese_seconds,
                                            surname_german_firsts, surname_german_seconds))
        else:
            names = generate_names_rand(gender, nobility, count,
                                        first_parts_male, second_parts_male,
                                        first_parts_female, second_parts_female,
                                        cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
                                        surname_italian_firsts, surname_italian_seconds,
                                        surname_polish_firsts, surname_polish_seconds,
                                        surname_polish_ends_male, surname_polish_ends_female,
                                        surname_japanese_firsts, surname_japanese_seconds,
                                        surname_romanian_firsts, surname_romanian_seconds,
                                        surname_chinese_firsts, surname_chinese_seconds,
                                        surname_german_firsts, surname_german_seconds)
    # serializer = NameSerializerSimple(names, many=True)
    # return Response(serializer.data, status.HTTP_200_OK)
    json = {'names': names}
    return Response(json, status.HTTP_200_OK)


@api_view(['GET'])
def get_namegen_version(request, format=None):
    json = {'app': 'namegen', 'version': version}
    return Response(json, status.HTTP_200_OK)
