# -*- coding: utf-8 -*-

from .models import *
from .forms2 import NamegenForm, Constants


import random
from random import choice


CONSONANTS = 'бвгджзйклмнпрстфхшщчц'
RIGHT_CONSONANTS = 'йнрс'
VOWELS = 'аеёиоуыэюя'


SLAVIC_CONNECTORS = {u'бр': [u'а'],             u'бм': [u'и'],                   u'вл': [u'и', u'о'],
                     u'вн': [u'а', u'и', u'я'], u'вс': [u'у', u'ы'],             u'вр': [u'е'],
                     u'вк': [u'и'],             u'вг': [u'и'],                   u'гж': [u'о'],
                     u'гн': [u'и'],             u'гт': [u'и'],                   u'гл': [u'е'],
                     u'дн': [u'и'],             u'дс': [u'и', u'о'],             u'др': [u'и', u'е'],
                     u'дв': [u'о', u'и', u'е'], u'дц': [u'и'],                   u'дж': [u'е'],
                     u'дм': [u'о'],             u'тф': [u'а'],                   u'жн': [u'е', u'и'],
                     u'жт': [u'а'],             u'жс': [u'е', u'и'],             u'жш': [u'и'],
                     u'мг': [u'а', u'е', u'и'], u'жк': [u'и'],                   u'жг': [u'и'],
                     u'жл': [u'а', u'и'],       u'зс': [u'и'],                   u'зр': [u'и'],
                     u'зл': [u'о', u'е'],       u'зт': [u'и'],                   u'зщ': [u'е', u'и'],
                     u'кж': [u'и'],             u'лш': [u'и', u'е'],             u'лн': [u'и'],
                     u'лт': [u'а'],             u'лм': [u'и'],                   u'лз': [u'и'],
                     u'лс': [u'и', u'о'],       u'лп': [u'и'],                   u'лв': [u'о', u'у', u'и', u'а'],
                     u'мн': [u'и'],             u'мз': [u'и'],                   u'нш': [u'и', u'е'],
                     u'нт': [u'и'],             u'нс': [u'а', u'и'],             u'нр': [u'а'],
                     u'нм': [u'и'],             u'нл': [u'и'],                   u'нж': [u'и', u'е'],
                     u'нв': [u'о'],             u'пл': [u'о'],                   u'рс': [u'и'],
                     u'рн': [u'о', u'и', u'е'], u'рф': [u'о'],                   u'рт': [u'и', u'о'],
                     u'рд': [u'и', u'у'],       u'рм': [u'и'],                   u'рц': [u'о', u'у', u'и'],
                     u'рл': [u'о', u'е', u'у'], u'рг': [u'о'],                   u'сн': [u'и'],
                     u'ср': [u'и', u'е'],       u'фн': [u'е', u'и'],             u'сб': [u'и'],
                     u'см': [u'и'],             u'сл': [u'е'],                   u'тн': [u'и'],
                     u'тр': [u'о'],             u'тл': [u'а', u'о'],             u'тс': [u'а', u'у', u'ы'],
                     u'тц': [u'и', u'ы'],       u'тм': [u'и'],                   u'тб': [u'и'],
                     u'фз': [u'и'],             u'фс': [u'и'],                   u'хн': [u'о'],
                     u'цн': [u'и', u'е'],       u'цс': [u'и', u'е'],             u'цр': [u'е'],
                     u'цб': [u'и'],             u'цш': [u'е', u'и'],             u'цх': [u'е'],
                     u'цт': [u'и'],             u'цд': [u'и'],                   u'цл': [u'и', u'е', u'а'],
                     u'чс': [u'е'],             u'чн': [u'и', u'е'],             u'шл': [u'у', u'е'],
                     u'рв': [u'о', u'у', u'а'], u'нф': [u'и'],                   u'шв': [u'о', u'е', u'а'],
                     u'жх': [u'и'],             u'тг': [u'о', u'и'],             u'дл': [u'и', u'у'],
                     u'чб': [u'о', u'и', u'е'], u'рж': [u'и', u'у', u'ы'],       u'хв': [u'о'],
                     u'зп': [u'и'],             u'вд': [u'и', u'е'],             u'зм': [u'и', u'е'],
                     u'сш': [u'и', u'е', u'у'], u'жф': [u'и'],                   u'гф': [u'о', u'у'],
                     u'нп': [u'у', u'и', u'о'], u'кд': [u'а', u'и', u'о'],       u'зд': [u'и'],
                     u'шм': [u'и'],             u'тш': [u'и'],                   u'бк': [u'е', u'а', u'и'],
                     u'шн': [u'и'],             u'гк': [u'и'],                   u'кн': [u'и', u'е'],
                     u'жв': [u'и'],             u'зн': [u'и', u'а'],             u'кш': [u'и', u'е', u'а', u'у'],
                     u'бс': [u'и', u'е', u'о'], u'нд': [u'и', u'е'],             u'бд': [u'о', u'и'],
                     u'цг': [u'е', u'и'],       u'гп': [u'о', u'у', u'е', u'и'], u'лр': [u'у', u'о', u'и'],
                     u'чт': [u'е', u'и'],       u'гш': [u'и', u'е'],             u'гс': [u'у', u'о'],
                     u'шч': [u'и', u'е', u'у'], u'дт': [u'о', u'у', u'и'],       u'бв': [u'о', u'а', u'и', u'у', u'е'],
                     u'рх': [u'а', u'и', u'о'], u'рш': [u'и', u'о'],             u'ст': [u'и'],
                     u'кв': [u'о', u'у'],       u'мд': [u'и', u'е'],             u'бт': [u'и', u'о', u'е'],
                     u'мр': [u'у', u'о', u'и'], u'вц': [u'и', u'е'],             u'зк': [u'и', u'е'],
                     u'шг': [u'у', u'и', u'е', u'о'],                            u'мц': [u'и', u'е'],
                     u'мф': [u'е', u'и'],       u'вш': [u'и', u'е'],             u'пс': [u'и', u'о'],
                     u'сз': [u'и', u'а', u'о', u'е'],                            u'рп': [u'и', u'е', u'о', u'у'],
                     u'тв': [u'и', u'е', u'о'], u'цм': [u'и', u'е', u'а'],       u'жщ': [u'е', u'и'],
                     u'шд': [u'о', u'и', u'е'], u'кл': [u'а', u'у'],             u'хл': [u'а', u'у'],
                     u'тк': [u'е', u'о', u'и'], u'пг': [u'о', u'е', u'и'],       u'кя': [u'и'],
                     u'гз': [u'о'],             u'жц': [u'и', u'е'],             u'вм': [u'и'],
                     u'нц': [u'и', u'е'],       u'цк': [u'и', u'е'],             u'чж': [u'и', u'е'],
                     u'жм': [u'и', u'е'],       u'гч': [u'о', u'и', u'е'],       u'жр': [u'и', u'о', u'е'],
                     u'нг': [u'и'],             u'дг': [u'о', u'и'],             u'цз': [u'и', u'ы'],
                     u'нз': [u'и', u'е', u'а'], u'лб': [u'и', u'а'],             u'сж': [u'и', u'е', u'а'],
                     u'фд': [u'и'],             u'рщ': [u'и', u'е', u'а'],       u'нк': [u'и'],
                     u'лг': [u'и'],             u'пж': [u'и', u'е', u'а'],       u'рз': [u'и'],
                     u'тз': [u'ы'],             u'цв': [u'и'],                   u'гв': [u'и', u'е'],
                     u'хс': [u'а'],             u'кс': [u'а'],                   u'фт': [u'а'],
                     u'жз': [u'е', u'и'],       u'дш': [u'и', u'е'],             u'вж': [u'и', u'е'],
                     u'фш': [u'и', u'е', u'а', u'у'],                            u'бз': [u'и', u'е', u'ы'],
                     u'св': [u'а', u'о'],       u'пр': [u'а', u'о', u'е'],       u'пм': [u'и', u'а', 'у'],
                     u'дп': [u'и', u'е'],       u'пц': [u'е', u'и'],             u'чш': [u'и', u'е'],
                     u'шз': [u'у', u'о', u'и'], u'нх': [u'и', u'е'],             u'лд': [u'е', u'и', u'у'],
                     u'сг': [u'о', u'и', u'е'], u'чп': [u'и', u'е'],             u'зц': [u'и', u'е'],
                     u'тч': [u'ы', u'и'],       u'чц': [u'и', u'е'],             u'дщ': [u'ы'],
                     u'сщ': [u'ы'],             u'тщ': [u'о', u'ы'],             u'дк': [u'е'],
                     u'кц': [u'а', u'е', u'и'], u'цф': [u'и', u'е'],             u'гд': [u'о', u'и'],
                     u'кг': [u'о', u'и', u'е'], u'чд': [u'и', u'е', u'а'],       u'шр': [u'у', u'о', u'и', u'е'],
                     u'бл': [u'е', u'у'],       u'хг': [u'о', u'и'],             u'ск': [u'и', u'е'],
                     u'тд': [u'о', u'у', u'е'], u'вч': [u'и', u'е', u'а', u'о', u'у', u'ы'],
                     u'хт': [u'е'],             u'шт': [u'е'],                   u'чм': [u'и', u'е'],
                     u'хд': [u'а', u'и', u'о'], u'нщ': [u'и', u'е', u'а', u'ы'], u'бц': [u'е', u'и'],
                     u'вз': [u'и'],             u'мк': [u'и', u'е'],             u'мв': [u'о'],
                     u'цч': [u'а', u'ы', u'е', u'и'],                            u'ря': [u'ь', u'и'],
                     u'чв': [u'е', u'о'],       u'чл': [u'е'],                   u'шц': [u'и', u'е', u'ы'],
                     u'пя': [u'и'],             u'мс': [u'ы', u'и', u'о'],       u'гя': [u'ь', u'е', u'и'],
                     u'ця': [u'ь', u'е', u'и'], u'вя': [u'ь', u'и', u'е'],       u'ня': [u'ь', u'и', u'е'],
                     u'пд': [u'и', u'а', u'о'], u'пт': [u'и', u'о', u'а'],       u'пв': [u'о', u'и'],
                     u'пк': [u'о', u'а'],       u'пн': [u'и', u'а', u'е', u'о'], }


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


FRENCH_CONNECTORS = {
    u'бб': [u'ье', u'ьи'],                         u'вб': [u'ье', u'ьи', u'и', u'е'],
    u'гб': [u'и', u'е', u'ье', u'ьи'],             u'дб': [u'и', u'е', u'ье', u'ьи', u'а'],
    u'жб': [u'ье', u'ье', u'и', u'е', u'а'],       u'зб': [u'е', u'о'],                     u'кб': [u'и', u'е', u'о'],
    u'мб': [u'е'],
    u'нб': [u'е'],                                 u'пб': [u'и', u'е', u'о'],               u'рб': [u'и', u'е', u'о'],
    u'сб': [u'е', u'и', u'ьи', u'ье'],
    u'тб': [u'о', u'е', u'и'],                     u'фб': [u'и', u'е'],                     u'хб': [u'и', u'е'],
    u'шб': [u'и', u'е'],
    u'бв': [u'и', u'е', u'ье', u'ьи'],             u'вв': [u'', u'и', u'е', u'ье', u'ьи'],
    u'гв': [u'и', u'е', u'ьи', u'ье'],             u'дв': [u'и', u'е', u'ьи', u'ье', u''],
    u'жв': [u'и', u'е', u'ьи', u'ье'],             u'зв': [u'е', u'ье'],
    u'кв': [u'и', u'е', u'ьи', u'ье'],             u'мв': [u'и', u'е', u'ьи', u'ье'],
    u'нв': [u'и', u'е', u'ьи', u'ье'],             u'пв': [u'и', u'е', u'ьи', u'ье'],       u'рв': [u'и', u'е', u'ье'],
    u'св': [u'и', u'е', u'ьи', u'ье'],
    u'тв': [u'и', u'е', u'ьи', u'ье'],             u'фв': [u'и', u'е', u'ьи', u'ье'],       u'хв': [u'е', u'и'],
    u'шв': [u'и', u'е'],
    u'бг': [u'и', u'е', u'ье'],                    u'вг': [u'и', u'е', u'ье'],              u'гг': [u'', u'ье'],
    u'дг': [u'и', u'е', u'ьи', u'ье'],
    u'жг': [u'и', u'е'],                           u'зг': [u'и', u'е'],
    u'кг': [u'и', u'е', u'а', u'ье', u'ьи'],       u'мг': [u'и', u'е'],
    u'нг': [u'и', u'е', u'ье', u'ьи'],             u'пг': [u'и', u'е'],                     u'рг': [u'и', u'е'],
    u'сг': [u'и', u'е', u'ье', u'ьи'],
    u'тг': [u'и', u'е', u'ье', u'ьи'],             u'фг': [u'и', u'е'],                     u'хг': [u'е', u'и'],
    u'шг': [u'и', u'е', u'ье', u'ьи'],
    u'бд': [u'е', u'е', u'о', u'а'],               u'вд': [u'и', u'е', u'ьи', u'ье'],
    u'гд': [u'и', u'е', u'о', u'ье'],              u'дд': [u'', u'и', u'о', u'е', u''],
    u'жд': [u'и', u'е', u'ьи', u'ье'],             u'зд': [u'и', u'е'],                     u'кд': [u'и', u'е', u'ье'],
    u'мд': [u'и', u'е', u'ьи', u'ье'],
    u'нд': [u'и', u'е', u'о', u'ье'],              u'пд': [u'и', u'е', u'ье'],              u'рд': [u'и', u'е', u'ье'],
    u'сд': [u'и', u'е'],
    u'тд': [u'и', u'е'],                           u'фд': [u'и', u'е'],                     u'хд': [u'и', u'е'],
    u'шд': [u'и', u'е'],
    u'бж': [u'и', u'е', u'ьи', u'о', u'ье'],       u'вж': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'дж': [u'и', u'е', u'ьи', u'ье'],             u'гж': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'жж': [u'', u'и', u'е', u'ьи', u'о', u'ье'],  u'зж': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'кж': [u'и', u'е', u'ьи', u'о', u'ье'],       u'мж': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'нж': [u'и', u'е', u'ьи', u'о', u'ье'],       u'пж': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'рж': [u'', u'и', u'е', u'ьи', u'о', u'ье'],  u'сж': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'тж': [u'и', u'е', u'ьи', u'о', u'ье'],       u'фж': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'хж': [u'и', u'е', u'ьи', u'о', u'ье'],       u'шж': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'бк': [u'и', u'е', u'ьи', u'о', u'ье'],       u'вк': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'гк': [u'и', u'е', u'ьи', u'о', u'ье'],       u'дк': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'жк': [u'и', u'е', u'ьи', u'о', u'ье'],       u'зк': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'кк': [u'', u'и', u'е', u'ьи', u'о', u'ье'],  u'мк': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'нк': [u'и', u'е', u'ьи', u'о', u'ье'],       u'пк': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'рк': [u'и', u'е', u'ьи', u'о', u'ье'],       u'ск': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'тк': [u'и', u'е', u'ьи', u'о', u'ье'],       u'фк': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'хк': [u'и', u'е', u'ьи', u'о', u'ье'],       u'шк': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'бл': [u'и', u'е', u'ьи', u'о', u'ье', u'а'], u'вл': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'гл': [u'и', u'е', u'ьи', u'о', u'ье', u''],  u'дл': [u'и', u'е', u'ьи', u'о', u'ье', u'а'],
    u'жл': [u'и', u'е', u'ьи', u'о', u'ье'],       u'зл': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'кл': [u'и', u'е', u'ьи', u'о', u'ье', u'а'], u'мл': [u'е', u'а'],
    u'нл': [u'и', u'е', u'ьи', u'о', u'ье'],       u'пл': [u'о', u'е', u'и'],
    u'рл': [u'е', u'и', u'а'],                     u'сл': [u'и', u'е'],
    u'тл': [u'и', u'е', u'а'],                     u'фл': [u'и', u'е'],
    u'хл': [u'и', u'е'],                           u'шл': [u'и', u'е'],
    u'бм': [u'и', u'е'],                           u'вм': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'гм': [u'и', u'е', u'ьи', u'о', u'ье'],       u'дм': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'жм': [u'и', u'е', u'ьи', u'о', u'ье'],       u'зм': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'км': [u'и', u'е', u'ьи', u'о', u'ье', u''],  u'мм': [u'и', u'е', u'ьи', u'о', u'ье', u''],
    u'нм': [u'и', u'е', u'ьи', u'о', u'ье'],       u'пм': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'рм': [u'и', u'е', u'ьи', u'о', u'ье', u''],  u'см': [u'и', u'е', u'ьи', u'о', u'ье', u''],
    u'тм': [u'и', u'е', u'ьи', u'о', u'ье'],       u'фм': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'хм': [u'и', u'е', u'ьи', u'о', u'ье'],       u'шм': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'бн': [u'и', u'е', u'ьи', u'о', u'ье'],       u'вн': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'гн': [u'и', u'е', u'ьи', u'о', u'ье'],       u'дн': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'жн': [u'и', u'е', u'ьи', u'о', u'ье'],       u'зн': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'кн': [u'и', u'е', u'ьи', u'о', u'ье'],       u'мн': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'нн': [u'', u'и', u'е', u'ьи', u'о', u'ье'],  u'пн': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'рн': [u'и', u'е', u'ьи', u'о', u'ье'],       u'сн': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'тн': [u'и', u'е', u'ьи', u'о', u'ье'],       u'фн': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'хн': [u'и', u'е', u'ьи', u'о', u'ье'],       u'шн': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'бр': [u'и', u'е', u'ьи', u'о', u'ье'],       u'вр': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'гр': [u'и', u'е', u'ьи', u'о', u'ье'],       u'др': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'жр': [u'и', u'е', u'ьи', u'о', u'ье'],       u'зр': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'кр': [u'и', u'е', u'ьи', u'о', u'ье'],       u'мр': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'нр': [u'', u'и', u'е', u'ьи', u'о', u'ье'],  u'пр': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'рр': [u'', u'и', u'е', u'ьи', u'о', u'ье'],  u'ср': [u'', u'и', u'е', u'ьи', u'о', u'ье'],
    u'тр': [u'и', u'е', u'ьи', u'о', u'ье'],       u'фр': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'хр': [u'и', u'е', u'ьи', u'о', u'ье'],       u'шр': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'бс': [u'и', u'е', u'ьи', u'о', u'ье'],       u'вс': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'гс': [u'и', u'е', u'ьи', u'о', u'ье'],       u'дс': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'жс': [u'и', u'е', u'ьи', u'о', u'ье'],       u'зс': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'кс': [u'и', u'е', u'ьи', u'о', u'ье'],       u'мс': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'нс': [u'и', u'е', u'ьи', u'о', u'ье'],       u'пс': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'рс': [u'и', u'е', u'ьи', u'о', u'ье'],       u'сс': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'тс': [u'и', u'е', u'ьи', u'о', u'ье'],       u'фс': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'хс': [u'и', u'е', u'ьи', u'о', u'ье'],       u'шс': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'бф': [u'и', u'е', u'ьи', u'о', u'ье'],       u'вф': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'гф': [u'и', u'е', u'ьи', u'о', u'ье'],       u'дф': [u'', u'и', u'е', u'ьи', u'о', u'ье'],
    u'жф': [u'и', u'е', u'ьи', u'о', u'ье'],       u'зф': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'кф': [u'и', u'е', u'ьи', u'о', u'ье'],       u'мф': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'нф': [u'и', u'е', u'ьи', u'о', u'ье'],       u'пф': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'рф': [u'и', u'е', u'ьи', u'о', u'ье'],       u'сф': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'тф': [u'и', u'е', u'ьи', u'о', u'ье'],       u'фф': [u'', u'и', u'е', u'ьи', u'о', u'ье'],
    u'хф': [u'и', u'е', u'ьи', u'о', u'ье'],       u'шф': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'бт': [u'и', u'е', u'ьи', u'о', u'ье'],       u'вт': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'гт': [u'и', u'е', u'ьи', u'о', u'ье'],       u'дт': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'жт': [u'и', u'е', u'ьи', u'о', u'ье'],       u'зт': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'кт': [u'и', u'е', u'ьи', u'о', u'ье'],       u'мт': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'нт': [u'и', u'е', u'ьи', u'о', u'ье'],       u'пт': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'рт': [u'и', u'е', u'ьи', u'о', u'ье'],       u'ст': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'тт': [u'', u'и', u'е', u'ьи', u'о', u'ье'],  u'фт': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'хт': [u'и', u'е', u'ьи', u'о', u'ье'],       u'шт': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'лб': [u'и', u'е', u'ьи', u'о', u'ье'],       u'лв': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'лг': [u'и', u'е', u'ьи', u'о', u'ье'],       u'лд': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'лж': [u'и', u'е', u'ьи', u'о', u'ье'],       u'лз': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'лк': [u'и', u'е', u'ьи', u'о', u'ье'],       u'лм': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'лн': [u'и', u'е', u'ьи', u'о', u'ье'],       u'лл': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'лп': [u'и', u'е', u'ьи', u'о', u'ье'],       u'лр': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'лс': [u'и', u'е', u'ьи', u'о', u'ье'],       u'лт': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'лф': [u'и', u'е', u'ьи', u'о', u'ье'],       u'лх': [u'и', u'е', u'ьи', u'о', u'ье'],
    u'лш': [u'и', u'е', u'ьи', u'о', u'ье'],       u'лй': [u'и', u'е', u'а', u'о'],
}


GERMAN_BLANK_CONNECTORS = [u'мм', u'рм', u'нт', u'рт', u'лф', u'лл', u'нх', u'нг', u'рн', u'лв',
                           u'лм', u'нр', u'лб', u'гл', u'см', u'зм', u'нн', u'гр', u'зб', u'сб',
                           u'тр', u'мг', u'мх', u'рм', u'нз', u'нс', u'бр', u'лм', u'гб', u'гн',
                           u'лх', u'лб', u'лв', u'др', u'гм', u'фх', u'фв', u'нк', u'нх', u'нг',
                           u'н',  u'тг', u'св', u'', u'', u'', u'', u'', u'',]


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
            Constants.ROMANIA, Constants.HUNGARY, Constants.CHINA, Constants.GERMANY, Constants.FRANCE]


def d100():
    return random.randint(1, 100)


def generate_name_scand_split(gender, nobility, first_parts_male, second_parts_male,
                              first_parts_female, second_parts_female):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = generate_name(MaleScand, FemaleScand, gender,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female)
    name += ' '
    middle_name = ''
    if nobility == Constants.NOBLE:
        if d100() <= 50:
            middle_name = generate_name(MaleScand, FemaleScand, Constants.MALE,
                                        first_parts_male, second_parts_male,
                                        first_parts_female, second_parts_female)
        else:
            middle_name = generate_name(MaleScand, FemaleScand, Constants.FEMALE,
                                        first_parts_male, second_parts_male,
                                        first_parts_female, second_parts_female)
        middle_name += ' '
    surname = generate_scand_surname(gender, first_parts_male, second_parts_male,
                                     first_parts_female, second_parts_female) + ' '
    return [name, middle_name, surname, gender_tail, noble_tail]


def generate_name_scand(gender, nobility, first_parts_male, second_parts_male,
                        first_parts_female, second_parts_female):
    [name, middle_name, surname,
     gender_tail, noble_tail] = generate_name_scand_split(gender, nobility, first_parts_male, second_parts_male,
                                                          first_parts_female, second_parts_female)
    return name + middle_name + surname + gender_tail + noble_tail


def generate_names_scand(gender, nobility, first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female, count=10):
    names = list()
    for i in range(count):
        names.append(generate_name_scand(gender, nobility,
                                         first_parts_male, second_parts_male,
                                         first_parts_female, second_parts_female))
    return names


def generate_name_latin(gender, nobility,
                        first_parts_male, second_parts_male,
                        first_parts_female, second_parts_female,
                        cognomen_first_parts, cognomen_second_parts_male,
                        cognomen_second_parts_female):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = generate_name(MaleLatin, FemaleLatin, gender,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female)
    name += ' '
    middle_name = ''
    if nobility == Constants.NOBLE:
        middle_name = generate_name(MaleLatin, FemaleLatin, gender,
                                    first_parts_male, second_parts_male,
                                    first_parts_female, second_parts_female)
        middle_name += ' '
        if d100() <= 50:
            middle_name = generate_name(MaleLatin, FemaleLatin, gender,
                                        first_parts_male, second_parts_male,
                                        first_parts_female, second_parts_female)
            middle_name += ' '
        if d100() <= 25:
            middle_name = generate_name(MaleLatin, FemaleLatin, gender,
                                        first_parts_male, second_parts_male,
                                        first_parts_female, second_parts_female)
            middle_name += ' '
    cognomen = generate_cognomen(gender, cognomen_first_parts,
                                 cognomen_second_parts_male,
                                 cognomen_second_parts_female)
    cognomen += ' '
    return name + middle_name + cognomen + gender_tail + noble_tail


def generate_names_latin(gender, nobility, count,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female,
                         cognomen_first_parts, cognomen_second_parts_male,
                         cognomen_second_parts_female):
    names = list()
    for i in range(count):
        names.append(generate_name_latin(gender, nobility, first_parts_male,
                                         second_parts_male, first_parts_female,
                                         second_parts_female, cognomen_first_parts,
                                         cognomen_second_parts_male, cognomen_second_parts_female))
    return names


def generate_name_spanish(gender, nobility,
                          first_parts_male, second_parts_male,
                          first_parts_female, second_parts_female):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = generate_name(MaleSpanish, FemaleSpanish, gender,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female)
    name += ' '
    if nobility == Constants.NOBLE:
        threshold = 75
    else:
        threshold = 50
    for i in range(choice([1, 2, 3])):
        if d100() <= threshold:
            name = generate_name(MaleSpanish, FemaleSpanish, gender,
                                 first_parts_male, second_parts_male,
                                 first_parts_female, second_parts_female)
            name += ' '

    surname = generate_spanish_surname(nobility, first_parts_male, second_parts_male,
                                       first_parts_female, second_parts_female) + ' '
    return name + surname + gender_tail + noble_tail


def generate_names_spanish(gender, nobility, count,
                           first_parts_male, second_parts_male,
                           first_parts_female, second_parts_female):
    names = list()
    for i in range(count):
        names.append(generate_name_spanish(gender, nobility,
                                           first_parts_male, second_parts_male,
                                           first_parts_female, second_parts_female))
    return names


def generate_name_italian(gender, nobility,
                          first_parts_male, second_parts_male,
                          first_parts_female, second_parts_female,
                          surnames_first_parts, surnames_second_part):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    first = u''
    second = u''
    while first.lower() == second.lower():
        if gender == Constants.MALE:
            first = choice(first_parts_male)[0]
            second = choice(second_parts_male)[0]
        else:
            first = choice(first_parts_female)[0]
            second = choice(second_parts_female)[0]
    name = correct_name_lazy(first, second) + ' '
    for i in range(choice([1, 2, 3])):
        first = u''
        second = u''
        while first.lower() == second.lower():
            if d100() <= 50:
                first = choice(first_parts_male)[0]
                second = choice(second_parts_male)[0]
            else:
                first = choice(first_parts_female)[0]
                second = choice(second_parts_female)[0]
        name += correct_name_lazy(first, second) + ' '
    surname = generate_italian_surname(nobility, surnames_first_parts, surnames_second_part)
    surname += ' '
    return name + surname + gender_tail + noble_tail


def generate_names_italian(gender, nobility, count,
                           first_parts_male, second_parts_male,
                           first_parts_female, second_parts_female,
                           surnames_first_parts, surnames_second_part):
    names = list()
    for i in range(count):
        names.append(generate_name_italian(gender, nobility,
                                           first_parts_male, second_parts_male,
                                           first_parts_female, second_parts_female,
                                           surnames_first_parts, surnames_second_part))
    return names


def generate_name_romanian(gender, nobility,
                           first_parts_male, second_parts_male,
                           first_parts_female, second_parts_female,
                           surname_firsts, surname_seconds, cognomen_firsts,
                           cognomen_seconds_male, cognomen_seconds_female):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = generate_romanian_name(gender,
                                  first_parts_male, second_parts_male,
                                  first_parts_female, second_parts_female) + ' '
    if nobility == Constants.NOBLE:
        name += generate_romanian_name(gender,
                                       first_parts_male, second_parts_male,
                                       first_parts_female, second_parts_female) + ' '
    if nobility == Constants.NOBLE:
        if d100() <= 50:
            surname = generate_romanian_surname(first_parts_male, second_parts_male,
                                                first_parts_female, second_parts_female,
                                                surname_firsts, surname_seconds)
        else:
            surname = generate_cognomen(gender, cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female)
    else:
        surname = generate_romanian_surname(first_parts_male, second_parts_male,
                                            first_parts_female, second_parts_female,
                                            surname_firsts, surname_seconds)
    surname += ' '
    return name + surname + gender_tail + noble_tail


def generate_names_romanian(gender, nobility, count,
                            first_parts_male, second_parts_male,
                            first_parts_female, second_parts_female,
                            surname_firsts, surname_seconds, cognomen_firsts,
                            cognomen_seconds_male, cognomen_seconds_female):
    names = list()
    for i in range(count):
        names.append(generate_name_romanian(gender, nobility,
                                            first_parts_male, second_parts_male,
                                            first_parts_female, second_parts_female,
                                            surname_firsts, surname_seconds, cognomen_firsts,
                                            cognomen_seconds_male, cognomen_seconds_female))
    return names


def generate_name_hungarian(gender, nobility,
                            first_parts_male, second_parts_male,
                            first_parts_female, second_parts_female,
                            surname_firsts, surname_seconds, cognomen_firsts,
                            cognomen_seconds_male, cognomen_seconds_female):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = generate_romanian_name(gender,
                                  first_parts_male, second_parts_male,
                                  first_parts_female, second_parts_female) + ' '
    if nobility == Constants.NOBLE:
        name += generate_romanian_name(gender,
                                       first_parts_male, second_parts_male,
                                       first_parts_female, second_parts_female) + ' '
    if nobility == Constants.NOBLE:
        if d100() <= 50:
            surname = generate_romanian_surname(first_parts_male, second_parts_male,
                                                first_parts_female, second_parts_female,
                                                surname_firsts, surname_seconds)
        else:
            surname = generate_cognomen(gender, cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female)
    else:
        surname = generate_romanian_surname(first_parts_male, second_parts_male,
                                            first_parts_female, second_parts_female,
                                            surname_firsts, surname_seconds)
    surname += ' '
    return name + surname + gender_tail + noble_tail


def generate_names_hungarian(gender, nobility, count,
                             first_parts_male, second_parts_male,
                             first_parts_female, second_parts_female,
                             surname_firsts, surname_seconds, cognomen_firsts,
                             cognomen_seconds_male, cognomen_seconds_female):
    names = list()
    for i in range(count):
        names.append(generate_name_hungarian(gender, nobility,
                                             first_parts_male, second_parts_male,
                                             first_parts_female, second_parts_female,
                                             surname_firsts, surname_seconds, cognomen_firsts,
                                             cognomen_seconds_male, cognomen_seconds_female))
    return names


def generate_name_chinese(gender, nobility,
                          first_parts_male, second_parts_male,
                          first_parts_female, second_parts_female,
                          surname_firsts, surname_seconds):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = generate_chinese_name(gender, first_parts_male, second_parts_male,
                                 first_parts_female, second_parts_female) + ' '
    surname = generate_chinese_surname(nobility, first_parts_male, second_parts_male,
                                       first_parts_female, second_parts_female,
                                       surname_firsts, surname_seconds) + ' '
    return name + surname + gender_tail + noble_tail


def generate_names_chinese(gender, nobility, count,
                           first_parts_male, second_parts_male,
                           first_parts_female, second_parts_female,
                           surname_firsts, surname_seconds):
    names = list()
    for i in range(count):
        names.append(generate_name_chinese(gender, nobility,
                                           first_parts_male, second_parts_male,
                                           first_parts_female, second_parts_female,
                                           surname_firsts, surname_seconds))
    return names


def generate_name_german(gender, nobility,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female,
                         surname_firsts, surname_seconds):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = generate_german_name(gender, first_parts_male, second_parts_male,
                                first_parts_female, second_parts_female) + ' '
    if nobility == Constants.NOBLE and d100() <= 50:
        if d100() <= 50:
            name += generate_german_name(Constants.MALE, first_parts_male, second_parts_male,
                                         first_parts_female, second_parts_female) + ' '
        else:
            name += generate_german_name(Constants.FEMALE, first_parts_male, second_parts_male,
                                         first_parts_female, second_parts_female) + ' '
    surname = generate_german_surname(nobility, surname_firsts, surname_seconds) + ' '
    return name + surname + gender_tail + noble_tail


def generate_names_german(gender, nobility, count,
                          first_parts_male, second_parts_male,
                          first_parts_female, second_parts_female,
                          surname_firsts, surname_seconds):
    names = list()
    for i in range(count):
        names.append(generate_name_german(gender, nobility,
                                          first_parts_male, second_parts_male,
                                          first_parts_female, second_parts_female,
                                          surname_firsts, surname_seconds))
    return names


def generate_name_french(gender, nobility,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female,
                         surname_firsts, surname_seconds):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = generate_french_name(gender, first_parts_male, second_parts_male, first_parts_female, second_parts_female)
    if nobility == Constants.NOBLE:
        if d100() <= 50:
            if d100() <= 50:
                name += ' ' + generate_french_name(Constants.MALE, first_parts_male, second_parts_male,
                                                   first_parts_female, second_parts_female) + ' '
            else:
                name += ' ' + generate_french_name(Constants.FEMALE, first_parts_male, second_parts_male,
                                                   first_parts_female, second_parts_female) + ' '
        else:
            name += ' '
    else:
        name += ' '
    surname = generate_french_surname(nobility, surname_firsts, surname_seconds)
    return name + surname + gender_tail + noble_tail


def generate_names_french(gender, nobility, count,
                          first_parts_male, second_parts_male,
                          first_parts_female, second_parts_female,
                          surname_firsts, surname_seconds):
    names = list()
    for i in range(count):
        names.append(generate_name_french(gender, nobility,
                                          first_parts_male, second_parts_male,
                                          first_parts_female, second_parts_female,
                                          surname_firsts, surname_seconds))
    return names


def prepare_data_rand_namegen():
    first_parts_male = dict()
    first_parts_male[Constants.SCAND] = MaleScand.objects.get_first_parts_list()
    first_parts_male[Constants.LATIN] = MaleLatin.objects.get_first_parts_list()
    first_parts_male[Constants.SPAIN] = MaleSpanish.objects.get_first_parts_list()
    first_parts_male[Constants.ITALY] = MaleItalian.objects.get_first_parts_list()
    first_parts_male[Constants.POLAND] = MalePolish.objects.get_first_parts_list()
    first_parts_male[Constants.JAPAN] = MaleJapanese.objects.get_first_parts_list()
    first_parts_male[Constants.ROMANIA] = MaleRomanian.objects.get_first_parts_list()
    first_parts_male[Constants.HUNGARY] = MaleHungarian.objects.get_first_parts_list()
    first_parts_male[Constants.CHINA] = MaleChinese.objects.get_first_parts_list()
    first_parts_male[Constants.GERMANY] = MaleGerman.objects.get_first_parts_list()
    first_parts_male[Constants.FRANCE] = MaleFrance.objects.get_first_parts_list()

    second_parts_male = dict()
    second_parts_male[Constants.SCAND] = MaleScand.objects.get_second_parts_list()
    second_parts_male[Constants.LATIN] = MaleLatin.objects.get_second_parts_list()
    second_parts_male[Constants.SPAIN] = MaleSpanish.objects.get_second_parts_list()
    second_parts_male[Constants.ITALY] = MaleItalian.objects.get_second_parts_list()
    second_parts_male[Constants.POLAND] = MalePolish.objects.get_second_parts_list()
    second_parts_male[Constants.JAPAN] = MaleJapanese.objects.get_second_parts_list()
    second_parts_male[Constants.ROMANIA] = MaleRomanian.objects.get_second_parts_list()
    second_parts_male[Constants.HUNGARY] = MaleHungarian.objects.get_second_parts_list()
    second_parts_male[Constants.CHINA] = MaleChinese.objects.get_second_parts_list()
    second_parts_male[Constants.GERMANY] = MaleGerman.objects.get_second_parts_list()
    second_parts_male[Constants.FRANCE] =  MaleFrance.objects.get_second_parts_list()

    first_parts_female = dict()
    first_parts_female[Constants.SCAND] = FemaleScand.objects.get_first_parts_list()
    first_parts_female[Constants.LATIN] = FemaleLatin.objects.get_first_parts_list()
    first_parts_female[Constants.SPAIN] = FemaleSpanish.objects.get_first_parts_list()
    first_parts_female[Constants.ITALY] = FemaleItalian.objects.get_first_parts_list()
    first_parts_female[Constants.POLAND] = FemalePolish.objects.get_first_parts_list()
    first_parts_female[Constants.JAPAN] = FemaleJapanese.objects.get_first_parts_list()
    first_parts_female[Constants.ROMANIA] = FemaleRomanian.objects.get_first_parts_list()
    first_parts_female[Constants.HUNGARY] = FemaleHungarian.objects.get_first_parts_list()
    first_parts_female[Constants.CHINA] = FemaleChinese.objects.get_first_parts_list()
    first_parts_female[Constants.GERMANY] = FemaleGerman.objects.get_first_parts_list()
    first_parts_female[Constants.FRANCE] = FemaleFrance.objects.get_first_parts_list()

    second_parts_female = dict()
    second_parts_female[Constants.SCAND] = FemaleScand.objects.get_second_parts_list()
    second_parts_female[Constants.LATIN] = FemaleLatin.objects.get_second_parts_list()
    second_parts_female[Constants.SPAIN] = FemaleSpanish.objects.get_second_parts_list()
    second_parts_female[Constants.ITALY] = FemaleItalian.objects.get_second_parts_list()
    second_parts_female[Constants.POLAND] = FemalePolish.objects.get_second_parts_list()
    second_parts_female[Constants.JAPAN] = FemaleJapanese.objects.get_second_parts_list()
    second_parts_female[Constants.ROMANIA] = FemaleRomanian.objects.get_second_parts_list()
    second_parts_female[Constants.HUNGARY] = FemaleHungarian.objects.get_second_parts_list()
    second_parts_female[Constants.CHINA] = FemaleChinese.objects.get_second_parts_list()
    second_parts_female[Constants.GERMANY] = FemaleGerman.objects.get_second_parts_list()
    second_parts_female[Constants.FRANCE] = FemaleFrance.objects.get_second_parts_list()

    cognomen_firsts = CognomenLatin.objects.get_first_parts_list()
    cognomen_seconds_male = CognomenLatin.objects.get_second_parts_male_list()
    cognomen_seconds_female = CognomenLatin.objects.get_second_parts_female_list()

    surname_italian_firsts = SurnamesItalian.objects.get_first_parts_list()
    surname_italian_seconds = SurnamesItalian.objects.get_second_parts_list()

    surname_polish_firsts = SurnamesPolish.objects.get_first_parts_list()
    surname_polish_seconds = SurnamesPolish.objects.get_second_parts_list()

    surname_polish_ends_male = SurnamesPolishEnd.objects.get_male_endings()
    surname_polish_ends_female = SurnamesPolishEnd.objects.get_female_endings()

    surname_japanese_firsts = SurnamesJapanese.objects.get_first_parts_list()
    surname_japanese_seconds = SurnamesJapanese.objects.get_second_parts_list()

    surname_romanian_firsts = SurnamesRomanian.objects.get_firsts_list()
    surname_romanian_seconds = SurnamesRomanian.objects.get_seconds_list()

    surname_chinese_firsts = SurnamesChinese.objects.get_first_parts_list()
    surname_chinese_seconds = SurnamesChinese.objects.get_second_parts_list()

    surname_german_firsts = SurnamesGerman.objects.get_first_parts_list()
    surname_german_seconds = SurnamesGerman.objects.get_second_parts_list()

    surname_french_firsts = SurnamesFrance.objects.get_first_parts_list()
    surname_french_seconds = SurnamesFrance.objects.get_second_parts_list()

    return [first_parts_male, second_parts_male, first_parts_female, second_parts_female,
            cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
            surname_italian_firsts, surname_italian_seconds,
            surname_polish_firsts, surname_polish_seconds,
            surname_polish_ends_male, surname_polish_ends_female,
            surname_japanese_firsts, surname_japanese_seconds,
            surname_romanian_firsts, surname_romanian_seconds,
            surname_chinese_firsts, surname_chinese_seconds,
            surname_german_firsts, surname_german_seconds,
            surname_french_firsts, surname_french_seconds]


def generate_name_rand(gender, nobility,
                       first_parts_male, second_parts_male,
                       first_parts_female, second_parts_female,
                       cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
                       surname_italian_firsts, surname_italian_seconds,
                       surname_polish_firsts, surname_polish_seconds,
                       surname_polish_ends_male, surname_polish_ends_female,
                       surname_japanese_firsts, surname_japanese_seconds,
                       surname_romanian_firsts, surname_romanian_seconds,
                       surname_chinese_firsts, surname_chinese_seconds,
                       surname_german_firsts, surname_german_seconds,
                       surname_french_firsts, surname_french_seconds):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = ''
    names_count = choice([1, 2, 3, 4])
    if nobility == Constants.SIMPLE:
        names_count = names_count // 2
        if names_count < 1:
            names_count += 1
    for i in range(names_count):
        lang = choice(LANG_IDS)
        [male, female] = determine_lang(lang)
        if lang == Constants.SPAIN and name == '':
            names_count += 1
        if lang == Constants.POLAND:
            name += generate_polish_name(gender, first_parts_male.get(lang), second_parts_male.get(lang),
                                         first_parts_female.get(lang), second_parts_female.get(lang)) + ' '
        elif lang == Constants.ROMANIA:
            name += generate_romanian_name(gender, first_parts_male.get(lang), second_parts_male.get(lang),
                                           first_parts_female.get(lang), second_parts_female.get(lang)) + ' '
        elif lang == Constants.HUNGARY:
            name += generate_hungarian_name(gender, first_parts_male.get(lang), second_parts_male.get(lang),
                                            first_parts_female.get(lang), second_parts_female.get(lang)) + ' '
        elif lang == Constants.CHINA:
            name += generate_chinese_name(gender, first_parts_male.get(lang), second_parts_male.get(lang),
                                          first_parts_female.get(lang), second_parts_female.get(lang)) + ' '
        elif lang == Constants.GERMANY:
            name += generate_german_name(gender, first_parts_male.get(lang), second_parts_male.get(lang),
                                         first_parts_female.get(lang), second_parts_female.get(lang)) + ' '
        elif lang == Constants.FRANCE:
            name += generate_french_name(gender, first_parts_male.get(lang), second_parts_male.get(lang),
                                         first_parts_female.get(lang), second_parts_female.get(lang)) + ' '
        else:
            name += generate_name(male, female, gender,
                                  first_parts_male.get(lang), second_parts_male.get(lang),
                                  first_parts_female.get(lang), second_parts_female.get(lang)) + ' '
    surname = ''
    lang = choice(LANG_IDS)
    if lang == Constants.SCAND:
        surname = generate_scand_surname(gender,
                                         first_parts_male.get(lang), second_parts_male.get(lang),
                                         first_parts_female.get(lang), second_parts_female.get(lang))
    elif lang == Constants.LATIN:
        surname = generate_cognomen(gender, cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female)
    elif lang == Constants.SPAIN:
        surname = generate_spanish_surname(nobility,
                                           first_parts_male.get(lang), second_parts_male.get(lang),
                                           first_parts_female.get(lang), second_parts_female.get(lang))
    elif lang == Constants.ITALY:
        surname = generate_italian_surname(nobility, surname_italian_firsts, surname_italian_seconds)
    elif lang == Constants.POLAND:
        surname = generate_polish_surname(gender, first_parts_male.get(lang), second_parts_male.get(lang),
                                          surname_polish_firsts, surname_polish_seconds,
                                          surname_polish_ends_male, surname_polish_ends_female)
    elif lang == Constants.JAPAN:
        surname = generate_japanese_surname(surname_japanese_firsts, surname_japanese_seconds)
        if nobility == Constants.NOBLE:
            surname += ' '
            return surname + name + gender_tail + noble_tail
    elif lang == Constants.ROMANIA or lang == Constants.HUNGARY:
        surname = generate_romanian_surname(first_parts_male.get(lang), second_parts_male.get(lang),
                                            first_parts_female.get(lang), second_parts_female.get(lang),
                                            surname_romanian_firsts, surname_romanian_seconds)
    elif lang == Constants.CHINA:
        surname = generate_chinese_surname(nobility,
                                           first_parts_male.get(lang), second_parts_male.get(lang),
                                           first_parts_female.get(lang), second_parts_female.get(lang),
                                           surname_chinese_firsts, surname_chinese_seconds)
    elif lang == Constants.GERMANY:
        surname = generate_german_surname(nobility, surname_german_firsts, surname_german_seconds)
    elif lang == Constants.FRANCE:
        surname = generate_french_surname(nobility, surname_french_firsts, surname_french_seconds)
    surname += ' '
    return name + surname + gender_tail + noble_tail


def determine_lang(lang):
    male = None
    female = None
    if lang == Constants.SCAND:
        male = MaleScand
        female = FemaleScand
    elif lang == Constants.LATIN:
        male = MaleLatin
        female = FemaleLatin
    elif lang == Constants.SPAIN:
        male = MaleSpanish
        female = FemaleSpanish
    elif lang == Constants.ITALY:
        male = MaleItalian
        female = FemaleItalian
    elif lang == Constants.POLAND:
        male = MalePolish
        female = SurnamesPolish
    elif lang == Constants.JAPAN:
        male = MaleJapanese
        female = FemaleJapanese
    elif lang == Constants.ROMANIA:
        male = MaleRomanian
        female = FemaleRomanian
    elif lang == Constants.HUNGARY:
        male = MaleHungarian
        female = FemaleHungarian
    elif lang == Constants.CHINA:
        male = MaleChinese
        female = FemaleChinese
    elif lang == Constants.GERMANY:
        male = MaleGerman
        female = FemaleGerman
    elif lang == Constants.FRANCE:
        male = MaleFrance
        female = FemaleFrance
    return [male, female]


def generate_names_rand(gender, nobility, count,
                        first_parts_male, second_parts_male,
                        first_parts_female, second_parts_female,
                        cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
                        surname_italian_firsts, surname_italian_seconds,
                        surname_polish_firsts, surname_polish_seconds,
                        surname_polish_ends_male, surname_polish_ends_female,
                        surname_japanese_firsts, surname_japanese_seconds,
                        surname_romanian_firsts, surname_romanian_seconds,
                        surname_chinese_firsts, surname_chinese_seconds,
                        surname_german_firsts, surname_german_seconds,
                        surname_french_firsts, surname_french_seconds):
    names = list()
    for i in range(count):
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
                                        surname_german_firsts, surname_german_seconds,
                                        surname_french_firsts, surname_french_seconds))
    return names


def generate_name_polish(gender, nobility,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female,
                         surname_polish_firsts, surname_polish_seconds,
                         surname_polish_ends_male, surname_polish_ends_female):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = ''
    name = generate_polish_name(gender,
                                first_parts_male, second_parts_male,
                                first_parts_female, second_parts_female)
    name += ' '
    if nobility == Constants.NOBLE:
        if d100() <= 50:
            name += generate_polish_name(Constants.MALE,
                                         first_parts_male, second_parts_male,
                                         first_parts_female, second_parts_female)
        else:
            name += generate_polish_name(Constants.FEMALE,
                                         first_parts_male, second_parts_male,
                                         first_parts_female, second_parts_female)
        name += ' '
    surname = generate_polish_surname(gender, first_parts_male, second_parts_male,
                                      surname_polish_firsts, surname_polish_seconds,
                                      surname_polish_ends_male, surname_polish_ends_female)
    surname += ' '
    return name + surname + gender_tail + noble_tail


def generate_names_polish(gender, nobility, count,
                          first_parts_male, second_parts_male,
                          first_parts_female, second_parts_female,
                          surname_polish_firsts, surname_polish_seconds,
                          surname_polish_ends_male, surname_polish_ends_female):
    names = list()
    for i in range(count):
        names.append(generate_name_polish(gender, nobility,
                                          first_parts_male, second_parts_male,
                                          first_parts_female, second_parts_female,
                                          surname_polish_firsts, surname_polish_seconds,
                                          surname_polish_ends_male, surname_polish_ends_female))
    return names


def generate_name_japanese(gender, nobility,
                           first_parts_male, second_parts_male,
                           first_parts_female, second_parts_female,
                           surname_firsts, surname_seconds):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = generate_name(MaleJapanese, FemaleJapanese, gender,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female)
    if gender == Constants.FEMALE and nobility == Constants.NOBLE:
        if d100() <= 50:
            name += u'химе'
    name += ' '
    surname = generate_japanese_surname(surname_firsts, surname_seconds)
    surname += ' '
    if nobility == Constants.NOBLE:
        return surname + name + gender_tail + noble_tail
    else:
        return name + surname + gender_tail + noble_tail


def generate_names_japanese(gender, nobility, count,
                            first_parts_male, second_parts_male,
                            first_parts_female, second_parts_female,
                            surname_firsts, surname_seconds):
    names = list()
    for i in range(count):
        names.append(generate_name_japanese(gender, nobility,
                                            first_parts_male, second_parts_male,
                                            first_parts_female, second_parts_female,
                                            surname_firsts, surname_seconds))
    return names


def generate_name_techno(gender, nobility, letters, text_numbers,
                         cults, ranks_simple, ranks_noble_magi,
                         ranks_noble_genetor, ranks_noble_logi,
                         rank_noble_artisan, rank_noble_myrmidon,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female,
                         cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
                         surname_italian_firsts, surname_italian_seconds,
                         surname_polish_firsts, surname_polish_seconds,
                         surname_polish_ends_male, surname_polish_ends_female,
                         surname_japanese_firsts, surname_japanese_seconds):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    namelength = 1
    title = u''
    cult_tail = MechanicusRanksNCults.objects.get_random_element(cults)
    if nobility == Constants.NOBLE:
        namelength += choice(range(2))
        if cult_tail == GENETOR:
            title = MechanicusRanksNCults.objects.get_random_element(ranks_noble_genetor)
        elif cult_tail == CYBERNETICA or cult_tail == REDUCTOR or cult_tail == TITANICA:
            dice = d100()
            if dice <= 20:
                title = MechanicusRanksNCults.objects.get_random_element(rank_noble_artisan)
            elif dice <= 40:
                title = MechanicusRanksNCults.objects.get_random_element(ranks_noble_magi)
            elif dice <= 60:
                title = MechanicusRanksNCults.objects.get_random_element(ranks_noble_genetor)
            elif dice <= 80:
                title = MechanicusRanksNCults.objects.get_random_element(rank_noble_myrmidon)
            else:
                title = MechanicusRanksNCults.objects.get_random_element(ranks_noble_logi)
            if cult_tail == TITANICA:
                cult_tail = u'Коллегии Титаника'
        elif cult_tail == MYRMIDON:
            title = MechanicusRanksNCults.objects.get_random_element(rank_noble_myrmidon)
        elif cult_tail == MAGI:
            title = MechanicusRanksNCults.objects.get_random_element(ranks_noble_magi)
        elif cult_tail == LOGI:
            title = MechanicusRanksNCults.objects.get_random_element(ranks_noble_logi)
        elif cult_tail == ARTISAN:
            title = MechanicusRanksNCults.objects.get_random_element(rank_noble_artisan)
    else:
        title = MechanicusRanksNCults.objects.get_random_element(ranks_simple)
    name = u''
    for i in range(namelength):
        if d100() <= 50:
            lang = choice(LANG_IDS)
            [male, female] = determine_lang(lang)
            if lang == Constants.POLAND:
                name += generate_polish_name(gender, first_parts_male.get(lang), second_parts_male.get(lang),
                                             first_parts_female.get(lang), second_parts_female.get(lang))
            elif lang == Constants.HUNGARY:
                name += generate_hungarian_name(gender, first_parts_male.get(lang), second_parts_male.get(lang),
                                                first_parts_female.get(lang), second_parts_female.get(lang))
            elif lang == Constants.ROMANIA:
                name += generate_romanian_name(gender, first_parts_male.get(lang), second_parts_male.get(lang),
                                               first_parts_female.get(lang), second_parts_female.get(lang))
            elif lang == Constants.CHINA:
                name += generate_chinese_name(gender, first_parts_male.get(lang), second_parts_male.get(lang),
                                              first_parts_female.get(lang), second_parts_female.get(lang))
            elif lang == Constants.GERMANY:
                name += generate_german_name(gender, first_parts_male.get(lang), second_parts_male.get(lang),
                                             first_parts_female.get(lang), second_parts_female.get(lang))
            else:
                name += generate_name(male, female, gender,
                                      first_parts_male.get(lang), second_parts_male.get(lang),
                                      first_parts_female.get(lang), second_parts_female.get(lang))
        else:
            dice = d100()
            if dice <= 33:
                name += generate_cognomen(gender, cognomen_firsts,
                                          cognomen_seconds_male, cognomen_seconds_female)
            elif dice <= 66:
                name += generate_italian_surname(Constants.SIMPLE, surname_italian_firsts, surname_italian_seconds)
            else:
                name += generate_japanese_surname(surname_japanese_firsts,surname_japanese_seconds)
        if d100() <= 66:
            name += ' '
        else:
            name += '-'
    name = name[:-1]
    tech_name = generate_designation_tech(gender, nobility, letters, text_numbers)
    return name + ' (' + tech_name + '), ' + title + ' из ' + cult_tail + ' ' + gender_tail + noble_tail


def generate_names_techno(gender, nobility, count, letters, text_numbers,
                          cults, ranks_simple, ranks_noble_magi,
                          ranks_noble_genetor, ranks_noble_logi,
                          rank_noble_artisan, rank_noble_myrmidon,
                          first_parts_male, second_parts_male,
                          first_parts_female, second_parts_female,
                          cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
                          surname_italian_firsts, surname_italian_seconds,
                          surname_polish_firsts, surname_polish_seconds,
                          surname_polish_ends_male, surname_polish_ends_female,
                          surname_japanese_firsts, surname_japanese_seconds):
    names = list()
    for i in range(count):
        names.append(generate_name_techno(gender, nobility, letters, text_numbers,
                                          cults, ranks_simple, ranks_noble_magi,
                                          ranks_noble_genetor, ranks_noble_logi,
                                          rank_noble_artisan, rank_noble_myrmidon,
                                          first_parts_male, second_parts_male,
                                          first_parts_female, second_parts_female,
                                          cognomen_firsts, cognomen_seconds_male,
                                          cognomen_seconds_female, surname_italian_firsts,
                                          surname_italian_seconds, surname_polish_firsts,
                                          surname_polish_seconds, surname_polish_ends_male,
                                          surname_polish_ends_female, surname_japanese_firsts,
                                          surname_japanese_seconds))
    return names


def prepare_lists_techno():
    ranks_simple = MechanicusRanksNCults.objects.get_ranks_simple()
    ranks_noble_magi = MechanicusRanksNCults.objects.get_ranks_noble_magi()
    ranks_noble_genetor = MechanicusRanksNCults.objects.get_ranks_noble_genetor()
    ranks_noble_logi = MechanicusRanksNCults.objects.get_ranks_noble_logi()
    ranks_noble_artisan = MechanicusRanksNCults.objects.get_ranks_noble_artisan()
    ranks_noble_myrmidon = MechanicusRanksNCults.objects.get_ranks_noble_myrmidon()
    cults = MechanicusRanksNCults.objects.get_cults()
    letters = TechDesignations.objects.get_letters()
    text_numbers = TechDesignations.objects.get_text_numbers()

    return [ranks_simple, ranks_noble_magi, ranks_noble_genetor,
            ranks_noble_logi, ranks_noble_artisan, ranks_noble_myrmidon,
            cults, letters, text_numbers]


def determine_gender(gender):
    if gender == Constants.RANDOM:
        if d100() <= 50:
            gender = Constants.MALE
        else:
            gender = Constants.FEMALE
    return gender


def determine_nobility(nobility):
    if nobility == Constants.RANDOM:
        if d100() <= 50:
            nobility = Constants.NOBLE
        else:
            nobility = Constants.SIMPLE
    return nobility


def resolve_randomness(gender, nobility):
    gender_tail = ''
    if gender == Constants.RANDOM:
        gender = determine_gender(gender)
        if gender == Constants.MALE:
            gender_tail = '(муж.)'
        else:
            gender_tail = '(жен.)'
    noble_tail = ''
    if nobility == Constants.RANDOM:
        nobility = determine_nobility(nobility)
        gender_tail += ' '
        if nobility == Constants.NOBLE:
            noble_tail = u'(благородное)'
        else:
            noble_tail = u'(простое)'
    return [nobility, gender, gender_tail, noble_tail]


def correct_name_lazy(first, second):
    if len(first) > 1 and first[-1:].lower() == u'ь':
        first = first[:-1]
    while len(first) > 1 and first[-1:].lower() in VOWELS:
        first = first[:-1]
    if second != u'' and first[-1:].lower() == second[0]:
        second = second[1:]
    if second != u'' and second[0] in CONSONANTS and first[-1:].lower() in CONSONANTS:
        dice = d100()
        if dice <= 25:
            first += u'и'
        elif dice <= 50:
            first += u'е'
        elif dice <= 75:
            first += u'а'
        else:
            first += u'у'
    return first + second


def generate_cognomen(gender, first_parts, male, female):
    first = u''
    second = u''
    while first.lower() == second.lower():
        first = choice(first_parts)[0]
        if gender == Constants.MALE:
            second = choice(male)[0]
        else:
            second = choice(female)[0]
    return correct_name_lazy(first, second)


def generate_name(lang_male, lang_female, gender,
                  first_parts_male, second_parts_male,
                  first_parts_female, second_parts_female):
    if lang_male == MaleLatin and lang_female == FemaleLatin\
       or lang_male == MaleSpanish and lang_female == FemaleSpanish:
        first = u''
        second = u''
        while first.lower() == second.lower():
            if gender == Constants.MALE:
                first = choice(first_parts_male)[0]
                second = choice(second_parts_male)[0]
            else:
                first = choice(first_parts_female)[0]
                second = choice(second_parts_female)[0]
            return correct_name_lazy(first, second)
    if gender == Constants.MALE:
        name = lang_male.objects.get_random_name(first_parts_male, second_parts_male)
    else:
        name = lang_female.objects.get_random_name(first_parts_female, second_parts_female)
    return name


def generate_scand_surname(gender, first_parts_male, second_parts_male,
                           first_parts_female, second_parts_female):
    surname = ''
    dice = d100()
    if dice <= 50:
        surname = MaleScand.objects.get_random_name(first_parts_male, second_parts_male)
    else:
        surname = FemaleScand.objects.get_random_name(first_parts_female, second_parts_female)
    dice = d100()
    if gender == Constants.MALE:
        if dice <= 50:
            surname += 'ссон'
        else:
            surname += 'снеф'
    else:
        if dice <= 50:
            surname += 'сдоттир'
        else:
            surname += 'сниз'
    return surname


def generate_spanish_surname(nobility, first_parts_male, second_parts_male,
                             first_parts_female, second_parts_female):
    surname = ''
    if nobility == Constants.NOBLE:
        threshold = 75
    else:
        threshold = 50
    if d100() <= 50:
        surname = MaleSpanish.objects.get_random_name(first_parts_male, second_parts_male)
    else:
        surname = FemaleSpanish.objects.get_random_name(first_parts_female, second_parts_female)
    if surname[-1:] in VOWELS:
        surname = surname[:-1]
    dice = d100()
    if dice <= 25:
        if surname[-1:] != 'л':
            if surname[-1:] not in RIGHT_CONSONANTS and surname[-1:] not in VOWELS:
                surname += 'и'
            if d100() <= 50:
                surname = correct_name_lazy(surname, 'хас')
            else:
                surname = correct_name_lazy(surname, 'гас')
        else:
            surname = correct_name_lazy(surname, 'ас')
    elif dice <= 50:
        if surname[-1:] != 'л':
            if surname[-1:] not in RIGHT_CONSONANTS and surname[-1:] not in VOWELS:
                surname += 'и'
            if d100() <= 50:
                surname = correct_name_lazy(surname, 'хес')
            else:
                surname = correct_name_lazy(surname, 'гес')
        else:
            surname += 'ес'
    elif dice <= 75:
        if surname[-1:] != 'з':
            if surname[-1:] not in 'тд':
                surname = correct_name_lazy(surname, 'сия')
            else:
                surname = correct_name_lazy(surname[:-1], 'ция')
        else:
            surname = correct_name_lazy(surname, 'ия')
    if d100() <= threshold:
        if nobility == 'N':
            if d100() <= 33:
                surname = ' ла ' + surname
            elif d100() <= 67:
                surname = ' де ' + surname
            else:
                surname = ' де ла ' + surname
        surname += '-и-'
        if d100() <= 50:
            surname += MaleSpanish.objects.get_random_name(first_parts_male, second_parts_male)
        else:
            surname += FemaleSpanish.objects.get_random_name(first_parts_female, second_parts_female)
        if surname[-1:] in VOWELS:
            surname = surname[:-1]
        dice = d100()
        if dice <= 25:
            if surname[-1:] != 'л':
                if surname[-1:] not in RIGHT_CONSONANTS and surname[-1:] not in VOWELS:
                    surname += 'и'
                if d100() <= 50:
                    surname = correct_name_lazy(surname, 'хас')
                else:
                    surname = correct_name_lazy(surname, 'гас')
            else:
                surname += correct_name_lazy(surname, 'ас')
        elif dice <= 50:
            if surname[-1:] != 'л':
                if surname[-1:] not in RIGHT_CONSONANTS and surname[-1:] not in VOWELS:
                    surname += 'и'
                if d100() <= 50:
                    surname = correct_name_lazy(surname, 'хес')
                else:
                    surname = correct_name_lazy(surname, 'гес')
            else:
                surname = correct_name_lazy(surname, 'ес')
        elif dice <= 75:
            if surname[-1:] != 'з':
                if surname[-1:] not in 'тд':
                    surname = correct_name_lazy(surname, 'сия')
                else:
                    surname = correct_name_lazy(surname[:-1], 'ция')
            else:
                surname = correct_name_lazy(surname, 'ия')
    else:
        if nobility == Constants.NOBLE:
            if d100() <= 33:
                surname = ' ла ' + surname
            elif d100() <= 67:
                surname = ' де ' + surname
            else:
                surname = ' де ла ' + surname
    return surname


def generate_italian_surname(nobility, first_parts, second_parts):
    first = u''
    second = u''
    while first.lower() == second.lower():
        first = choice(first_parts)[0]
        second = choice(second_parts)[0]
    surname = correct_name_lazy(first, second)
    if nobility == Constants.NOBLE:
        if d100() <= 50:
            if surname[1:].lower() in VOWELS:
                if d100() <= 50:
                    surname = 'Д\'' + surname
                else:
                    surname = 'ди ' + surname
            else:
                surname = 'ди ' + surname
        else:
            surname = 'ла ' + surname
    return surname


def generate_name_parts(gender,
                        first_parts_male, second_parts_male,
                        first_parts_female, second_parts_female):
    first = ''
    second = ''
    while first.lower() == second.lower():
        if gender == Constants.MALE:
            first = choice(first_parts_male)[0]
            second = choice(second_parts_male)[0]
        else:
            first = choice(first_parts_female)[0]
            second = choice(second_parts_female)[0]
    return [first, second]


def generate_polish_name(gender,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female):
    [first, second] = generate_name_parts(gender,
                                          first_parts_male, second_parts_male,
                                          first_parts_female, second_parts_female)
    return correct_polish_name(first, second)


def generate_romanian_name(gender,
                           first_parts_male, second_parts_male,
                           first_parts_female, second_parts_female):
    [first, second] = generate_name_parts(gender,
                                          first_parts_male, second_parts_male,
                                          first_parts_female, second_parts_female)
    return correct_romanian_name(first, second)


def generate_hungarian_name(gender,
                            first_parts_male, second_parts_male,
                            first_parts_female, second_parts_female):
    [first, second] = generate_name_parts(gender,
                                          first_parts_male, second_parts_male,
                                          first_parts_female, second_parts_female)
    return correct_hungarian_name(first, second)


def correct_name(first, second, connectors, blank_connectors, surname=False):
    if surname and first[-1:] == u'ь':
        first = first[:-1]
    if second != u'':
        if first[-1:] == second[0]:
            second = second[1:]
        if second != u'':
            pair = first[-1:] + second[0]
        else:
            pair = first[-1:]
        if not surname:
            if pair in blank_connectors:
                if d100() <= 50:
                    if pair in connectors.keys() and connectors.get(pair.lower()) != u'':
                        first += choice(connectors.get(pair.lower()))
            elif pair in connectors.keys() and connectors.get(pair.lower()) != u'':
                first += choice(connectors.get(pair.lower()))
        elif pair in connectors.keys() and connectors.get(pair.lower()) != u'':
            first += choice(connectors.get(pair.lower()))
    return first + second


def correct_polish_name(first, second, surname=False):
    return correct_name(first, second, SLAVIC_CONNECTORS, SLAVIC_BLANK_CONNECTORS, surname)


def correct_romanian_name(first, second, surname=False):
    return correct_name(first, second, ROMANIAN_CONNECTORS, ROMANIAN_BLANK_CONNECTORS, surname)


def correct_hungarian_name(first, second, surname=False):
    return correct_name(first, second, ROMANIAN_CONNECTORS, ROMANIAN_BLANK_CONNECTORS, surname)


def correct_french_name(first, second, surname=False):
    return correct_name(first, second, FRENCH_CONNECTORS, [], surname)


def generate_polish_surname(gender, first_parts_male, second_parts_male,
                            first_parts_surname, second_parts_surname,
                            male_endings, female_endings):
    if d100() <= 50:
        return generate_polish_nb_surname(gender, first_parts_male, second_parts_male,
                                          male_endings, female_endings)
    else:
        return generate_polish_misc_surname(gender, first_parts_surname, second_parts_surname,
                                            male_endings, female_endings)


def generate_polish_nb_surname(gender, first_parts, second_parts, male_endings, female_endings):
    surname = ''
    surname = generate_polish_name(Constants.MALE, first_parts,
                                   second_parts, first_parts, second_parts)
    if gender == Constants.MALE:
        ending = SurnamesPolishEnd.objects.random_ending(male_endings)
    else:
        ending = SurnamesPolishEnd.objects.random_ending(female_endings)
    if surname[-1:] == u'й':
        surname = surname[:-1]
    if ending != u'' and ending[0] in VOWELS:
        while surname[-1:] in VOWELS:
            surname = surname[:-1]
    if ending != '' and surname[-1:] == ending[0]:
        ending = ending[1:]
    return correct_polish_name(surname, ending, surname=True)


def generate_polish_misc_surname(gender, first_parts, second_parts, male_endings, female_endings):
    surname = ''
    surname = generate_polish_name(Constants.MALE, first_parts, second_parts, first_parts, second_parts)
    if gender == Constants.MALE:
        ending = SurnamesPolishEnd.objects.random_ending(male_endings)
    else:
        ending = SurnamesPolishEnd.objects.random_ending(female_endings)
    if surname[-1:] == u'й':
        surname = surname[:-1]
    if ending != '' and ending[0] in VOWELS:
        while surname[-1:] in VOWELS:
            surname = surname[:-1]
    if ending != '' and surname[-1:] == ending[0]:
        ending = ending[1:]
    return correct_polish_name(surname, ending, surname=True)


def generate_japanese_surname(first_parts, second_parts):
    return SurnamesJapanese.objects.get_random_name(first_parts, second_parts)


def generate_romanian_surname(firsts_male, seconds_male,
                              firsts_female, seconds_female,
                              surname_firsts, surname_seconds):
    if d100() <= 50:
        return generate_romanian_nb_surname(firsts_male, seconds_male,
                                            firsts_female, seconds_female,
                                            surname_seconds)
    else:
        return generate_romanian_misc_surname(surname_firsts, surname_seconds)


def generate_romanian_nb_surname(firsts_male, seconds_male,
                                 firsts_female, seconds_female,
                                 surname_seconds):
    if d100() <= 50:
        gender = Constants.MALE
    else:
        gender = Constants.FEMALE
    name = generate_romanian_name(gender,
                                  firsts_male, seconds_male,
                                  firsts_female, seconds_female)
    while name[-1:] in VOWELS:
        name = name[:-1]
    return correct_romanian_name(name, SurnamesRomanian.objects.get_random_element(surname_seconds))


def generate_romanian_misc_surname(firsts, seconds):
    return correct_romanian_name(SurnamesRomanian.objects.get_random_element(firsts),
                                 SurnamesRomanian.objects.get_random_element(seconds))


def generate_designation_tech(gender, nobility,
                              letters, text_numbers):
    designation_length = choice(range(5)) + 2
    if nobility == Constants.NOBLE:
        designation_length += choice(range(3)) + 2
    designation = u''
    prev = ''
    for i in range(designation_length):
        if d100() <= 50:
            if prev == 'L' and i > 0:
                designation += '-'
            elif i > 0 and prev != 'N':
                if designation[-1:] not in VOWELS:
                    if gender == Constants.MALE:
                        dice = d100()
                        if dice <= 50:
                            designation += u'ус '
                        else:
                            designation += u'иум '
                    else:
                        dice = d100()
                        if dice <= 50:
                            designation += u'а '
                        else:
                            designation += u'ина '
                else:
                    designation += ' '
            elif i > 0:
                designation += ' '
            designation += TechDesignations.objects.get_random_element(letters)
            prev = 'L'
        elif d100() <= 50:
            if prev == 'D' and i > 0:
                designation += '-'
            elif i > 0:
                designation += ' '
            designation += TechDesignations.objects.get_random_element(text_numbers)
            prev = 'D'
        else:
            if prev == 'N' and i > 0:
                if d100() <= 50:
                    designation += u'/'
                else:
                    designation += u'-'
            elif i > 0:
                if d100() <= 50:
                    designation += u' '
                else:
                    dice = d100()
                    if dice <= 50:
                        designation += u'-'
                    else:
                        designation += u'/'
            number = str(random.randint(0, 9999))
            while len(number) < 4:
                number = u'0' + number
            designation += number
            prev = 'N'
    return designation


def generate_chinese_name(gender, first_parts_male, second_parts_male,
                          first_parts_female, second_parts_female):
    name = u''
    if gender == Constants.MALE:
        name = choice(first_parts_male)[0]
        if len(name) > 4:
            threshold = 33
        else:
            threshold = 50
        if d100() <= threshold:
            name += choice(second_parts_male)[0].lower()
    else:
        name = choice(first_parts_female)[0]
        if len(name) > 4:
            threshold = 33
        else:
            threshold = 50
        if d100() <= threshold:
            name += choice(second_parts_female)[0].lower()
    return name


def generate_german_name(gender, first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female):
    first = u''
    second = u''
    while first == second:
        if gender == Constants.MALE:
            first = choice(first_parts_male)[0]
            second = choice(second_parts_male)[0]
        else:
            first = choice(first_parts_female)[0]
            second = choice(second_parts_female)[0]
    return correct_name(first, second, GERMAN_CONNECTORS, GERMAN_BLANK_CONNECTORS)


def generate_german_surname(nobility, first_parts, second_parts):
    first = u''
    second = u''
    while first.lower() == second:
        first = choice(first_parts)[0]
        second = choice(second_parts)[0]
    surname = correct_name(first, second, GERMAN_CONNECTORS, GERMAN_BLANK_CONNECTORS)
    if nobility == Constants.NOBLE:
        surname = 'фон ' + surname
    return surname


def generate_french_name(gender,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female):
    first_part = u''
    second_part = u''
    while first_part == second_part:
        if gender == Constants.MALE:
            first_part = choice(first_parts_male)[0]
            second_part = choice(second_parts_male)[0]
        else:
            first_part = choice(first_parts_female)[0]
            second_part = choice(second_parts_female)[0]
    return correct_french_name(first_part, second_part)


def generate_french_surname(nobility, first_parts, second_parts):
    surname = u''
    threshold = 50
    if nobility == Constants.NOBLE:
        surname_prefixes = [u'де ', u'ди ', u'дю ', u'ла ', u'д\'', u'ле ', u'де ла ']
        if d100() <= threshold:
            surname += choice(surname_prefixes)
        threshold = 70
    first = u''
    second = u''
    while first == second:
        first = choice(first_parts)[0]
        second = choice(second_parts)[0]
    surname += correct_french_name(first, second, True)
    if d100() <= threshold:
        surname += '-'
        first = u''
        second = u''
        while first == second:
            first = choice(first_parts)[0]
            second = choice(second_parts)[0]
        surname += correct_french_name(first, second, True)
    return surname


def generate_chinese_surname(nobility, first_parts_male, second_parts_male,
                             first_parts_female, second_parts_female,
                             surname_firsts, surname_seconds):
    if nobility == Constants.NOBLE:
        if d100() <= 50:
            surname = choice(surname_firsts)[0]
            if len(surname) > 4:
                threshold = 33
            else:
                threshold = 50
            if d100() <= threshold:
                surname += choice(surname_seconds)[0].lower()
        else:
            if d100() <= 50:
                surname = choice(first_parts_male)[0]
                if len(surname) > 4:
                    threshold = 33
                else:
                    threshold = 50
                if d100() <= threshold:
                    if d100() <= 50:
                        surname += choice(second_parts_male)[0].lower()
                    else:
                        surname += choice(second_parts_female)[0].lower()
            else:
                surname = choice(first_parts_female)[0]
                if len(surname) > 4:
                    threshold = 33
                else:
                    threshold = 50
                if d100() <= threshold:
                    if d100() <= 50:
                        surname += choice(second_parts_female)[0].lower()
                    else:
                        surname += choice(second_parts_male)[0].lower()
    else:
        if d100() <= 50:
            surname = choice(first_parts_male)[0]
            if len(surname) > 4:
                threshold = 33
            else:
                threshold = 50
            if d100() <= threshold:
                if d100() <= 50:
                    surname += choice(second_parts_male)[0].lower()
                else:
                    surname += choice(second_parts_female)[0].lower()
        else:
            surname = choice(first_parts_female)[0]
            if len(surname) > 4:
                threshold = 33
            else:
                threshold = 50
            if d100() <= threshold:
                if d100() <= 50:
                    surname += choice(second_parts_female)[0].lower()
                else:
                    surname += choice(second_parts_male)[0].lower()
    return surname


def create_names(lang, gender, nobility, count):
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
         surname_german_firsts, surname_german_seconds,
         surname_french_firsts, surname_french_seconds] = prepare_data_rand_namegen()

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
    elif lang == Constants.FRANCE:
        first_parts_male = MaleFrance.objects.get_first_parts_list()
        second_parts_male = MaleFrance.objects.get_second_parts_list()

        first_parts_female = FemaleFrance.objects.get_first_parts_list()
        second_parts_female = FemaleFrance.objects.get_second_parts_list()

        surname_firsts = SurnamesFrance.objects.get_first_parts_list()
        surname_seconds = SurnamesFrance.objects.get_second_parts_list()

        if count == 1:
            names.append(generate_name_french(gender, nobility,
                                              first_parts_male, second_parts_male,
                                              first_parts_female, second_parts_female,
                                              surname_firsts, surname_seconds))
        else:
            names = generate_names_french(gender, nobility, count,
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
         surname_german_firsts, surname_german_seconds,
         surname_french_firsts, surname_french_seconds] = prepare_data_rand_namegen()
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
                                            surname_german_firsts, surname_german_seconds,
                                            surname_french_firsts, surname_french_seconds))
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
                                        surname_german_firsts, surname_german_seconds,
                                        surname_french_firsts, surname_french_seconds)
    return names
