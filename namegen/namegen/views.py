# -*- coding: utf-8 -*-
from random import choice

from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from .models import MaleScand, FemaleScand, MaleLatin, FemaleLatin, CognomenLatin,\
    MaleSpanish, FemaleSpanish, MaleItalian, FemaleItalian, SurnamesItalian,\
    MalePolish, FemalePolish, SurnamesPolish, SurnamesPolishEnd,\
    MaleJapanese, FemaleJapanese, SurnamesJapanese, TechDesignations,\
    MechanicusRanksNCults, MaleRomanian, FemaleRomanian, MaleHungarian, FemaleHungarian,\
    SurnamesRomanian, MaleChinese, FemaleChinese, SurnamesChinese
from .forms2 import NamegenForm, Constants

import random

version = '1.10.5'

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
            Constants.ROMANIA, Constants.HUNGARY, Constants.CHINA]


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
                 surname_chinese_firsts, surname_chinese_seconds] = prepare_data_rand_namegen()

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
            elif lang == Constants.RANDOM:
                [first_parts_male, second_parts_male, first_parts_female, second_parts_female,
                 cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
                 surname_italian_firsts, surname_italian_seconds,
                 surname_polish_firsts, surname_polish_seconds,
                 surname_polish_ends_male, surname_polish_ends_female,
                 surname_japanese_firsts, surname_japanese_seconds,
                 surname_romanian_firsts, surname_romanian_seconds,
                 surname_chinese_firsts, surname_chinese_seconds] = prepare_data_rand_namegen()
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
                                                    surname_chinese_firsts, surname_chinese_seconds))
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
                                                surname_chinese_firsts, surname_chinese_seconds)

            return render(request, 'index.html', {'form': form, 'names': names, 'version': version, })
    else:
        form = NamegenForm()

        return render(request, 'index.html', {'form': form, 'version': version, })


def d100():
    return random.randint(1, 100)


def generate_name_scand(gender, nobility, first_parts_male, second_parts_male,
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

    return [first_parts_male, second_parts_male, first_parts_female, second_parts_female,
            cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
            surname_italian_firsts, surname_italian_seconds,
            surname_polish_firsts, surname_polish_seconds,
            surname_polish_ends_male, surname_polish_ends_female,
            surname_japanese_firsts, surname_japanese_seconds,
            surname_romanian_firsts, surname_romanian_seconds,
            surname_chinese_firsts, surname_chinese_seconds]


def generate_name_rand(gender, nobility,
                       first_parts_male, second_parts_male,
                       first_parts_female, second_parts_female,
                       cognomen_firsts, cognomen_seconds_male, cognomen_seconds_female,
                       surname_italian_firsts, surname_italian_seconds,
                       surname_polish_firsts, surname_polish_seconds,
                       surname_polish_ends_male, surname_polish_ends_female,
                       surname_japanese_firsts, surname_japanese_seconds,
                       surname_romanian_firsts, surname_romanian_seconds,
                       surname_chinese_firsts, surname_chinese_seconds):
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
                        surname_chinese_firsts, surname_chinese_seconds):
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
                                        surname_chinese_firsts, surname_chinese_seconds))
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
    if len(first) > 1 and first[-1:] == u'ь':
        first = first[:-1]
    while len(first) > 1 and first[-1:] in VOWELS:
        first = first[:-1]
    if second != u'' and first[-1:] == second[0] and first[-1:] in VOWELS:
        second = second[1:]
    if second != u'' and second[0] in CONSONANTS and first[-1:] in CONSONANTS:
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
                    if pair in connectors.keys():
                        first += choice(connectors.get(pair.lower()))
            elif pair in connectors.keys():
                first += choice(connectors.get(pair.lower()))
        elif pair in connectors.keys():
            first += choice(connectors.get(pair.lower()))
    return first + second


def correct_polish_name(first, second, surname=False):
    return correct_name(first, second, SLAVIC_CONNECTORS, SLAVIC_BLANK_CONNECTORS, surname)


def correct_romanian_name(first, second, surname=False):
    return correct_name(first, second, ROMANIAN_CONNECTORS, ROMANIAN_BLANK_CONNECTORS, surname)


def correct_hungarian_name(first, second, surname=False):
    return correct_name(first, second, ROMANIAN_CONNECTORS, ROMANIAN_BLANK_CONNECTORS, surname)


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


# class Corrector:
#    CORRECTIONS = [(u'аа', u'а'), (u'ее', u'е'), (u'ёё', u'ё'), (u'ёе', u'е'),
#                   (u'ээ', u'э'), (u'еэ', u'э'), (u'эе', u'эйе'), (u'аё', u'айо'),
#                   (u'яя', u'я'), (u'оо', u'о'), (u'', u''), (u'', u'')]
