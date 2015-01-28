from django import forms
from django.utils.translation import ugettext_lazy as _
from main.parameters import *
import models


class PWSForm(forms.ModelForm):
    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=15, label=_('Number'))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=50, label=_('Name'))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=30, label=_('City'))
    water_source = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'uk-width-1-1'}),
                                          queryset=models.SourceType.objects.all(), label=_('Source type'),
                                          empty_label=_('None'))
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'uk-width-1-1'}), max_length=255, required=False)

    class Meta:
        model = models.PWS


class CustomerForm(forms.ModelForm):
    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=15, label=_('Number'))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=50, label=_('Name'))
    code = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'uk-width-1-1'}),
                                  queryset=models.CustomerCode.objects.all(), label=_('Code'), empty_label=_('None'))
    address1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=30,
                               label=_('Address 1'))
    address2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=30,
                               label=_('Address 2'), required=False)
    apt = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=15,
                          label=_('Appartment'), required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=15, label=_('City'))
    state = forms.TypedChoiceField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), choices=STATES,
                                   label=_('State'), empty_value=_('None'))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=15, label=_('ZIP'))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=15, label=_('Phone'),
                            required=False)
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'uk-width-1-1'}), max_length=255, label=_('Notes'),
                            required=False)

    class Meta:
        model = models.Customer