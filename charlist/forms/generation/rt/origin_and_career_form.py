# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form

from charlist.flyweights.rt_flyweights import RTFacade


class OriginAndCareerForm(Form):
    def __init__(self, facade: RTFacade, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hw_choices = list()
        for tag, hw in facade.rt_homeworlds().items():
            hw_choices.append((tag, hw.get_name_en()))
        self.fields['hw_id'].choices = hw_choices
        birthright_choices = list()
        for tag, br in facade.birthrights().items():
            name = br.name().get('en')
            if br.cost() > 0:
                name += ' (' + str(br.cost()) + ' XP)'
            birthright_choices.append((tag, name))
        self.fields['br_id'].choices = birthright_choices
        lures = list()
        for tag, lure in facade.lures().items():
            name = lure.name().get('en')
            if lure.cost() > 0:
                name += ' (' + str(lure.cost()) + ' XP)'
            lures.append((tag, name))
        self.fields['lure_id'].choices = lures
        trials = list()
        for tag, trial in facade.trials().items():
            name = trial.name().get('en')
            if trial.cost() > 0:
                name += ' (' + str(trial.cost()) + ' XP)'
            trials.append((tag, name))
        self.fields['trial_id'].choices = trials
        motivations = list()
        for tag, motive in facade.motivations().items():
            name = motive.name().get('en')
            if motive.cost() > 0:
                name += ' (' + str(motive.cost()) + ' XP)'
            motivations.append((tag, name))
        self.fields['motivation_id'].choices = motivations
        careers = list()
        for tag, career in facade.careers().items():
            careers.append((tag, career.name().get('en')))
        self.fields['career_id'].choices = careers

    hw_id = forms.ChoiceField(label=u'Homeworld')
    br_id = forms.ChoiceField(label=u'Birthright')
    lure_id = forms.ChoiceField(label=u'Lure of the Void')
    trial_id = forms.ChoiceField(label=u'Trial or Travail')
    motivation_id = forms.ChoiceField(label=u'Motivation')
    career_id = forms.ChoiceField(label=u'Career')


