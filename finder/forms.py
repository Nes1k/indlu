# -*- coding: utf-8 -*-
from django import forms
from geopy import geocoders
from .models import Preferences, Place
SORT_BY = ((0, '-----'), (1, 'Ceny malejąco'), (2, 'Ceny rosnąco'))


class PreferencesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PreferencesForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Preferences
        exclude = ['user']


class PlaceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(PlaceForm, self).clean()
        city = cleaned_data.get('city')
        street = cleaned_data.get('street')

        g = geocoders.GoogleV3(domain='maps.google.pl')
        location = g.geocode('%s, %s' % (city, street))

        if location is None:
            raise forms.ValidationError(
                'Niestety nie potrafimy wskazać podanej lokalizacji nieruchomości.')

    class Meta:
        model = Place
        exclude = ['preferences', 'location']


class SearchForm(PreferencesForm):
    sort_by = forms.CharField(label='Sortuj', max_length=10,
                              widget=forms.Select(choices=SORT_BY))
