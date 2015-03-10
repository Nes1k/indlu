# -*- coding: utf-8 -*-
from django import forms
from .models import Advertisement


class AdvertisementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdvertisementForm, self).__init__(*args, **kwargs)
        self.fields['building'].widget = forms.HiddenInput()
        self.fields['building'].label = ''
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(AdvertisementForm, self).clean()
        building = cleaned_data.get('building')
        rooms = building.rooms_set.all()
        if rooms.count() == 0:
            self.add_error(
                None, 'Dodaj pomieszczenia do nieruchomości aby móc wystawić ogłoszenie.')
        else:
            image = False
            total = 0
            for room in rooms:
                total += room.free_places
                if room.roomimage_set.all():
                    image = True
                    break
            if not total:
                self.add_error(
                    None, 'Pomieszczenie które Dodałeś nie mają wolnych miejsc.')
            if not image:
                self.add_error(
                    None, 'Dodaj zdjęcie aby móc umieścić ogłoszenie.')

    class Meta:
        model = Advertisement
        exclude = ['free_places', 'image']
