# -*- coding: utf-8 -*-
from django import forms
from .models import Building, Rooms, Item
from geopy import geocoders
import hashlib
import random


class BuildingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BuildingForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(BuildingForm, self).clean()
        city = cleaned_data.get('city')
        street_address = cleaned_data.get('street_address')

        g = geocoders.GoogleV3(domain='maps.google.pl')
        location = g.geocode('%s, %s' % (city, street_address))

        if location is None:
            raise forms.ValidationError(
                'Niestety nie potrafimy wskazać podanej lokalizacji nieruchomości.')

    class Meta:
        model = Building
        fields = ['country', 'street_address',
                  'postal_code', 'city', 'buidling_type', 'name']


class RoomForm(forms.ModelForm):
    equipment = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Item.objects.all())

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_area(self):
        area = self.cleaned_data.get('area')
        if area <= 0:
            raise forms.ValidationError(
                'Podano nieprawidłową powierzchnie pomieszczenia.')

        return area

    class Meta:
        model = Rooms
        fields = ['rooms_type', 'name', 'area',
                  'free_places', 'equipment']


class ImageForm(forms.Form):
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        hash_name = hashlib.sha1(
            str(random.random()).encode(encoding='utf-8')).hexdigest()[:40]

        name = image.name.split('.')
        name[0] = hash_name
        name = '.'.join(name)
        image.name = name
        return image
