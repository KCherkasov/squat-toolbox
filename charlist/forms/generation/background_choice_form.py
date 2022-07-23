# -*- coding: utf-8 -*-

from django.forms import Form
from django import forms
from charlist.constants.tags import *

BACKGROUNDS = ([BACKGROUND_ADMINISTRATUM, 'Adeptus Administratum'],
               [BACKGROUND_ASTRA_TELEPATHICA, 'Adeptus Astra Telepathica'],
               [BACKGROUND_ARBITES, 'Adeptus Arbites'],       [BACKGROUND_MECHANICUS, 'Adeptus Mechanicus'],
               [BACKGROUND_MINISTORUM, 'Adeptus Ministorum'], [BACKGROUND_ASTRA_MILITARUM, 'Astra Militarum'],
               [BACKGROUND_OUTCAST, 'Outcast'],               [BACKGROUND_HERETEK, 'Heretek'],
               [BACKGROUND_NAVY, 'Imperial Navy'],            [BACKGROUND_RT_FLEET, 'Rogue Trader fleet'],
               [BACKGROUND_EXCORCISED, 'Exorcised'],          [BACKGROUND_SORORITAS, 'Adepta Sororitas'],
               [BACKGROUND_MUTANT, 'Mutant'])

BACKGROUNDS_LIST = [BACKGROUND_ADMINISTRATUM, BACKGROUND_ASTRA_TELEPATHICA, BACKGROUND_ARBITES, BACKGROUND_MECHANICUS,
                    BACKGROUND_MINISTORUM, BACKGROUND_ASTRA_MILITARUM, BACKGROUND_OUTCAST, BACKGROUND_HERETEK,
                    BACKGROUND_NAVY, BACKGROUND_RT_FLEET, BACKGROUND_EXCORCISED, BACKGROUND_SORORITAS,
                    BACKGROUND_MUTANT]


class BackgroundChoiceForm(Form):
    backgrounds = forms.ChoiceField(verbose_name='Предыстория', choices=BACKGROUNDS)

