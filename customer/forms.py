# -*- coding: utf-8 -*-
from django import forms
from .models import CustomerUser


class CustomerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomerUser
        fields = ['country', 'first_name', 'last_name',
                  'street', 'postal_code', 'city', 'phone', 'email']


class PrimaryContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PrimaryContactForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomerUser
        fields = ['first_name', 'email', 'phone']
